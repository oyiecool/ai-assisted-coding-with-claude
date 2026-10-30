from hypothesis import given, strategies as st

@given(h=st.integers(0, 99), m=st.integers(0, 59), s=st.integers(0, 59))
def test_roundtrip(h, m, s):
    text = f"{h}h{m}m{s}s"
    assert parse_duration(text) == h * 3600 + m * 60 + s
