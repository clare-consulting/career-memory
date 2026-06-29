from connector_manager import ConnectorManager


def print_banner() -> None:
    """
    Print the Career Memory application banner.
    """
    print("=" * 40)
    print("Career Memory")
    print("=" * 40)


def main() -> None:
    """
    Run the Career Memory connector loading workflow.
    """
    print_banner()

    manager = ConnectorManager()
    events = manager.load_all_events()

    print(f"Loaded {len(events)} career events.")


if __name__ == "__main__":
    main()
