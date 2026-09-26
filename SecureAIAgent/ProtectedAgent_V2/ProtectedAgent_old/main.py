from agent import Agent


# ========================================
# Create Protected Agent
# ========================================

agent = Agent()


# ========================================
# Interactive Loop
# ========================================

print("========================================")
print("Autonomous AI Assistant Agent")
print("========================================")

print(
    "輸入 exit / quit / q 可以離開。"
)


while True:

    user_input = input(
        "\nUser："
    ).strip()

    # ----------------------------------------
    # Exit
    # ----------------------------------------

    if user_input.lower() in [
        "exit",
        "quit",
        "q"
    ]:

        print(
            "\nAgent 結束。"
        )

        break

    # ----------------------------------------
    # Empty Input
    # ----------------------------------------

    if not user_input:

        continue

    # ----------------------------------------
    # Agent Run
    # ----------------------------------------

    result = agent.run(
        user_input
    )

    print(
        "\n===== Final Result ====="
    )

    print(
        result
    )