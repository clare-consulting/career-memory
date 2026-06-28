from connector_manager import ConnectorManager


def main():

    print("=" * 40)
    print("Career Memory")
    print("=" * 40)

    manager = ConnectorManager()

    events = manager.load_all_events()

    print()
    print(f"Loaded {len(events)} career events.")


if __name__ == "__main__":
    main()