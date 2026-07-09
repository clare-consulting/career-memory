from typing import Dict

from analytics import AnalyticsEngine
from connector_manager import ConnectorManager
from recommendation import RecommendationEngine


def print_banner() -> None:
    """
    Print the Career Memory application banner.
    """
    print("=" * 40)
    print("Career Memory")
    print("=" * 40)


def print_count_section(title: str, counts: Dict[str, int]) -> None:
    """
    Print one analytics count section.
    """
    print()
    print(title)
    if not counts:
        print("None")
        return
    for label, count in counts.items():
        print(f"{label:.<20}{count}")


def print_analytics_report(events_count: int, analytics: AnalyticsEngine) -> None:
    """
    Print the console analytics report.
    """
    print()
    print(f"Loaded {events_count} Career Events")
    print_count_section("Sources", analytics.count_by_source())
    print_count_section("Agencies", analytics.count_by_agency())
    print_count_section("Interaction Types", analytics.count_by_interaction_type())


def print_morning_brief(events_count: int, analytics: AnalyticsEngine, recommendation_engine: RecommendationEngine) -> None:
    """
    Print the Career Memory Morning Brief.
    """
    print()
    print("-" * 40)
    print("Good Morning")
    print()
    print("Career Memory Morning Brief")
    print("-" * 40)
    print()
    print("Career Events Loaded")
    print(events_count)
    print_count_section("Top Agencies", analytics.count_by_agency())
    print_count_section("Top Interaction Types", analytics.count_by_interaction_type())
    print()
    print("Estimated Time Saved Today")
    print("15 minutes")
    print()
    print("Today's Recommendation")

    recommendation = recommendation_engine.get_recommendation()
    if recommendation is None:
        print("No actionable recruiter items today.")
    else:
        print(recommendation.headline)
        print()
        print("Reason")
        for line in recommendation.reason_lines:
            print(line)


def main() -> None:
    """
    Run the Career Memory connector loading and analytics workflow.
    """
    print_banner()
    manager = ConnectorManager()
    events = manager.load_all_events()
    analytics = AnalyticsEngine(events)
    recommendation_engine = RecommendationEngine(events)
    print_analytics_report(len(events), analytics)
    print_morning_brief(len(events), analytics, recommendation_engine)


if __name__ == "__main__":
    main()