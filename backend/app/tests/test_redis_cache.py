"""Tests for Redis cache functionality"""

from unittest.mock import patch
from app.core.cache import (
    RedisCache,
    cached,
    redis_cache,
    clear_user_cache,
    clear_resume_cache,
)


class TestRedisCache:
    """Test Redis cache operations"""

    def test_redis_connection(self):
        """Test Redis connection is established"""
        cache = RedisCache()
        assert cache.client is not None

    def test_set_and_get(self):
        """Test basic set and get operations"""
        test_key = "test_key_123"
        test_value = {"name": "test", "value": 42}

        # Set value
        success = redis_cache.set(test_key, test_value, 60)
        assert success is True

        # Get value
        retrieved = redis_cache.get(test_key)
        assert retrieved == test_value

        # Cleanup
        redis_cache.delete(test_key)

    def test_get_nonexistent_key(self):
        """Test getting non-existent key returns None"""
        result = redis_cache.get("nonexistent_key_xyz")
        assert result is None

    def test_delete_key(self):
        """Test key deletion"""
        test_key = "delete_test_key"
        test_value = "delete_test_value"

        # Set and verify
        redis_cache.set(test_key, test_value, 60)
        assert redis_cache.get(test_key) == test_value

        # Delete and verify
        redis_cache.delete(test_key)
        assert redis_cache.get(test_key) is None

    def test_cached_decorator(self):
        """Test cached decorator functionality"""
        call_count = 0

        @cached(60)
        def expensive_function(x, y):
            nonlocal call_count
            call_count += 1
            return x + y

        # First call should execute function
        result1 = expensive_function(1, 2)
        assert result1 == 3
        assert call_count == 1

        # Second call should use cache
        result2 = expensive_function(1, 2)
        assert result2 == 3
        assert call_count == 1  # Should not increment

        # Different args should execute function
        result3 = expensive_function(2, 3)
        assert result3 == 5
        assert call_count == 2

    def test_cache_with_complex_data(self):
        """Test caching with complex data structures"""
        complex_data = {
            "users": [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}],
            "metadata": {"total": 2, "page": 1},
            "nested": {"deep": {"value": "test"}},
        }

        redis_cache.set("complex_test", complex_data, 60)
        retrieved = redis_cache.get("complex_test")

        assert retrieved == complex_data
        redis_cache.delete("complex_test")

    @patch("app.core.cache.redis.Redis")
    def test_redis_connection_failure(self, mock_redis):
        """Test handling of Redis connection failure"""
        mock_redis.side_effect = Exception("Connection failed")

        cache = RedisCache()
        assert cache.client is None

        # Operations should fail gracefully
        assert cache.get("test") is None
        assert cache.set("test", "value") is False
        assert cache.delete("test") is False

    def test_clear_pattern(self):
        """Test pattern-based cache clearing"""
        # Set multiple keys with pattern
        redis_cache.set("user_1_profile", {"id": 1}, 60)
        redis_cache.set("user_2_profile", {"id": 2}, 60)
        redis_cache.set("other_data", {"data": "test"}, 60)

        # Clear user pattern
        redis_cache.clear_pattern("user_*_profile")

        # Verify user keys are cleared but other data remains
        assert redis_cache.get("user_1_profile") is None
        assert redis_cache.get("user_2_profile") is None
        assert redis_cache.get("other_data") == {"data": "test"}

        # Cleanup
        redis_cache.delete("other_data")

    def test_cache_management_utilities(self):
        """Test cache management utility functions"""
        # Set test data
        redis_cache.set("user_123_data", {"user": "test"}, 60)
        redis_cache.set("resume_456_data", {"resume": "test"}, 60)

        # Test clear functions
        clear_user_cache(123)
        clear_resume_cache(456)

        # Verify data is cleared
        assert redis_cache.get("user_123_data") is None
        assert redis_cache.get("resume_456_data") is None
