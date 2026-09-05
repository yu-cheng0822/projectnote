from agent import Agent


def main():
    agent = Agent()

    user_input = input("User：")

    answer = agent.run(user_input)

    print("AI：")
    print(answer)


if __name__ == "__main__":
    main()