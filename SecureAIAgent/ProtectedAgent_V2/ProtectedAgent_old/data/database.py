class Database:

    def __init__(self):

        # ========================================
        # 帳號資料
        # ========================================

        self.accounts = [
            {
                "account_id": "A001",
                "username": "alice",
                "role": "user"
            },
            {
                "account_id": "A002",
                "username": "bob",
                "role": "admin"
            },
            {
                "account_id": "A003",
                "username": "charlie",
                "role": "user"
            }
        ]

        # ========================================
        # 使用者資料
        # ========================================

        self.users = [
            {
                "user_id": "U001",
                "name": "Alice",
                "email": "alice@example.com",
                "phone": "0912-345-678"
            },
            {
                "user_id": "U002",
                "name": "Bob",
                "email": "bob@example.com",
                "phone": "0923-456-789"
            },
            {
                "user_id": "U003",
                "name": "Charlie",
                "email": "charlie@example.com",
                "phone": "0934-567-890"
            }
        ]

        # ========================================
        # 敏感資料
        # ========================================

        self.sensitive_data = [
            {
                "user_id": "U001",
                "address": "Taipei",
                "private_information": "Private Data A"
            },
            {
                "user_id": "U002",
                "address": "Taichung",
                "private_information": "Private Data B"
            },
            {
                "user_id": "U003",
                "address": "Kaohsiung",
                "private_information": "Private Data C"
            }
        ]

    # ========================================
    # 查詢帳號
    # ========================================

    def get_accounts(
        self,
        account_id=None,
        username=None
    ):

        results = self.accounts

        if account_id is not None:
            results = [
                account
                for account in results
                if account["account_id"].lower()
                == account_id.lower()
            ]

        if username is not None:
            results = [
                account
                for account in results
                if account["username"].lower()
                == username.lower()
            ]

        return results

    # ========================================
    # 查詢使用者
    # ========================================

    def get_users(
        self,
        user_id=None,
        name=None
    ):

        results = self.users

        if user_id is not None:
            results = [
                user
                for user in results
                if user["user_id"].lower()
                == user_id.lower()
            ]

        if name is not None:
            results = [
                user
                for user in results
                if user["name"].lower()
                == name.lower()
            ]

        return results

    # ========================================
    # 查詢敏感資料
    # ========================================

    def get_sensitive_data(
        self,
        user_id=None
    ):

        results = self.sensitive_data

        if user_id is not None:
            results = [
                data
                for data in results
                if data["user_id"].lower()
                == user_id.lower()
            ]

        return results


# ============================================
# Database Test
# ============================================

if __name__ == "__main__":

    database = Database()

    print("===== Database Test =====")

    # ----------------------------------------
    # 全部帳號
    # ----------------------------------------

    print("\nAll Accounts:")

    print(
        database.get_accounts()
    )

    # ----------------------------------------
    # 指定帳號
    # ----------------------------------------

    print("\nAccount: alice")

    print(
        database.get_accounts(
            username="alice"
        )
    )

    # ----------------------------------------
    # 全部使用者
    # ----------------------------------------

    print("\nAll Users:")

    print(
        database.get_users()
    )

    # ----------------------------------------
    # 指定使用者
    # ----------------------------------------

    print("\nUser: Alice")

    print(
        database.get_users(
            name="Alice"
        )
    )

    # ----------------------------------------
    # 全部敏感資料
    # ----------------------------------------

    print("\nAll Sensitive Data:")

    print(
        database.get_sensitive_data()
    )

    # ----------------------------------------
    # 指定使用者的敏感資料
    # ----------------------------------------

    print("\nSensitive Data: U001")

    print(
        database.get_sensitive_data(
            user_id="U001"
        )
    )