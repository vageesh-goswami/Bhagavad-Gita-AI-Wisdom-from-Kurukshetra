import pytest

from core.config import RetrievalConfig


def test_default_retrieval_config_is_valid() -> None:
    RetrievalConfig().validate()


@pytest.mark.parametrize(
    "config",
    [
        RetrievalConfig(chunk_size=100),
        RetrievalConfig(chunk_size=500, chunk_overlap=500),
        RetrievalConfig(top_k=0),
    ],
)
def test_invalid_retrieval_config_is_rejected(config: RetrievalConfig) -> None:
    with pytest.raises(ValueError):
        config.validate()
