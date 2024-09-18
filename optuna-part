import os

from stable_baselines3.common.callbacks import BaseCallback

from stable_baselines3.common import env_checker



class TrainAndLoggingCallback(BaseCallback):

    def __init__(self, check_freq, save_path, verbose=1):
        super(TrainAndLoggingCallback, self).__init__(verbose)
        self.check_freq = check_freq
        self.save_path = save_path

    def _init_callback(self):
        if self.save_path is not None:
            os.makedirs(self.save_path, exist_ok=True)

    def _on_step(self):
        if self.n_calls % self.check_freq == 0:
            model_path = os.path.join(self.save_path, 'best_model_{}'.format(self.n_calls))
            self.model.save(model_path)

        return True


callback = TrainAndLoggingCallback(check_freq=20000, save_path=CHECKPOINT_DIR)

from stable_baselines3.common.evaluation import evaluate_policy

from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import DummyVecEnv, VecFrameStack

env = RPGEnv(render_mode='human')
         
        
env = Monitor(env, LOG_DIR)

env = DummyVecEnv([lambda: env])

env = VecFrameStack(env, 4, channels_order='first')
 

best_params = {'ent_coef':0.1,'n_steps': 6976, 'gamma': 0.9649380160580032, 'learning_rate': 2.1396052807539818e-05, 'clip_range': 0.11522141646185477, 'gae_lambda': 0.8382597083533241}

model = PPO("MultiInputPolicy", env, tensorboard_log=LOG_DIR, verbose=1, **best_params)

model.learn(total_timesteps=150_000, callback=callback)

def objective(trial):
    try:
        # Define hyperparameter search space
        n_steps = trial.suggest_int('n_steps', 2048, 8192)
        gamma = trial.suggest_loguniform('gamma', 0.8, 0.999)
        learning_rate = trial.suggest_loguniform('learning_rate', 1e-6, 1e-4)
        clip_range = trial.suggest_uniform('clip_range', 0.08, 0.3)
        gae_lambda = trial.suggest_uniform('gae_lambda', 0.8, 0.99)

        env = RPGEnv()
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        env = Monitor(env, LOG_DIR)

        env = DummyVecEnv([lambda: env])

        env = VecFrameStack(env, 4, channels_order='first')

        model = PPO("CnnPolicy", 
                    env, 
                    tensorboard_log=LOG_DIR, 
                    verbose=0, 
                    n_steps=n_steps, 
                    gamma=gamma, 
                    learning_rate=learning_rate, 
                    clip_range=clip_range, 
                    gae_lambda=gae_lambda)
        
        model.learn(total_timesteps=50_000)

        mean_reward, _ = evaluate_policy(model, env, n_eval_episodes=5)
        env.close()

        SAVE_PATH = os.path.join(OPT_DIR, 'trial_{}_best_model'.format(trial.number))

        model.save(SAVE_PATH)

 
        
        return mean_reward

    except Exception as e:
        print(f"Exception occurred: {e}")
        return -5000


study = optuna.create_study(direction='maximize')

 
study.optimize(objective, n_trials=13, n_jobs=1)
 
print("Best hyperparameters: ", study.best_params)
