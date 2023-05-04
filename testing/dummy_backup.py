class DummySqliteBackup:
    def backup_db(self) -> None:
        pass

    def get_database_name(self) -> str:
        return ""


class DummySqliteRestore:
    def restore_db(self, date_str: str = "") -> None:
        pass
