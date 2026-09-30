from edge_ai_surveillance.policy import EventPolicy


def test_policy_filters_confidence_and_labels() -> None:
    policy = EventPolicy(
        labels=["animal"],
        min_confidence=0.7,
        cooldown_seconds=10,
    )

    assert not policy.should_emit("person", 0.99, now=0)
    assert not policy.should_emit("animal", 0.69, now=0)
    assert policy.should_emit("animal", 0.90, now=0)


def test_policy_applies_cooldown_per_label() -> None:
    policy = EventPolicy(
        labels=["animal"],
        min_confidence=0.5,
        cooldown_seconds=10,
    )

    assert policy.should_emit("animal", 0.9, now=0)
    assert not policy.should_emit("animal", 0.9, now=5)
    assert policy.should_emit("animal", 0.9, now=10)
