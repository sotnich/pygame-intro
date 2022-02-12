import os
import numpy as np
from ai.mygymenvironment import MyGymEnvironment
from ai.q_training import train_q_table

NUM_EPISODES = 10000                    # number of training iterations
MAX_STEPS = 1000                        # per episode in training
WATCH_WHILE_TRAIN = False               # show game while training
MAX_WATCH_STEPS = 10000                 # per episode in final watch


def watch_trained(env, q_table):
    print(f"Showing trained agent")
    state = env.reset()
    for s in range(MAX_WATCH_STEPS):
        action = np.argmax(q_table[state, :])
        new_state, reward, done, info = env.step(action)
        env.render()
        state = new_state
        if done:
            return

def main():
    q_file_name = f"../qtables/q-{NUM_EPISODES}-{MAX_STEPS}.npy"

    env = MyGymEnvironment()
    env.mute_game_on()

    if os.path.isfile(q_file_name):
        print(f"Training file: {q_file_name}")
        print(f"Training file exists. Loading it instead of training.")
        q_table = np.load(q_file_name)
    else:
        q_table = train_q_table(env, WATCH_WHILE_TRAIN, NUM_EPISODES, MAX_STEPS)
        os.makedirs("../qtables", exist_ok=True)
        np.save(q_file_name, q_table)
        print(f"Saved training file: {q_file_name}")

    env.mute_game_off()
    watch_trained(env, q_table)

    env.close()


if __name__ == '__main__':
    main()
