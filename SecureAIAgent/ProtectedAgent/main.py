
from agent import Agent


def main():

    # ========================================
    # 1. 建立 AI Agent
    # ========================================

    agent = Agent()

    # ========================================
    # 2. 接收使用者輸入
    # ========================================

    user_input = input("User：")

    # ========================================
    # 3. 執行 Agent
    # ========================================

    answer = agent.run(user_input)

    # ========================================
    # 4. 顯示自然語言回答
    # ========================================

    print("\n===== AI Response =====")

    # ----------------------------------------
    # 有使用工具
    # ----------------------------------------

    if answer["tool"] is not None:

        execution = answer["execution"]

        if execution["success"]:

            tool_name = answer["tool"]
            result = execution["result"]

            if tool_name == "calculator":

                print(
                    f"AI：計算結果是 {result}。"
                )

            else:

                print(
                    f"AI：工具 {tool_name} 執行成功，"
                    f"結果為 {result}。"
                )

        else:

            print(
                "AI：抱歉，這次操作未能執行。"
            )

            print(
                "原因：",
                execution["reason"]
            )

    # ----------------------------------------
    # 沒有使用工具
    # ----------------------------------------

    else:

        print(
            "AI：",
            answer["decision"]
        )


if __name__ == "__main__":

    main()