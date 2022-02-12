import random
import numpy as np


def train_episode(max_steps, env, q_table, watch, learning_rate, discount_rate, epsilon):
    state = env.reset()
    for i in range(max_steps):

        # exploration-exploitation tradeoff
        if random.uniform(0, 1) < epsilon:
            # explore
            action = env.action_space.sample()
        else:
            # exploit
            action = np.argmax(q_table[state, :])

        # take action and observe reward
        new_state, reward, done, info = env.step(action)

        # Q-learning algorithm
        q_table[state, action] = q_table[state, action] + learning_rate * (
                reward + discount_rate * np.max(q_table[new_state, :]) - q_table[state, action]
        )

        # Update to our new state
        state = new_state

        if watch:
            env.render("fast_human")

        if done:
            break

    return q_table


def train_q_table(env, watch, num_episodes, max_steps, learning_rate=0.9,
                  discount_rate=0.8, epsilon_start=1.0, decay_rate=0.005):

    print(f"Training the agent")

    # initialize q-table
    state_size = env.observation_space.n
    action_size = env.action_space.n
    q_table = np.zeros((state_size, action_size))

    epsilon = epsilon_start
    for episode in range(num_episodes):
        # sys.stdout.flush()
        print(f"Start {episode}/{num_episodes} train episode", end='\r')
        train_episode(max_steps, env, q_table, watch, learning_rate, discount_rate, epsilon)
        # Decrease epsilon
        epsilon = np.exp(-decay_rate * episode)

    print(f"Training completed over {num_episodes} episodes")

    return q_table
