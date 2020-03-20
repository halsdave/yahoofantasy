from collections import namedtuple
from unittest import TestCase
from yahoofantasy.stats.utils import get_stat_and_value, get_stat_from_stat_list


StatResult = namedtuple('StatObj', ['stat_id', 'value'])


class TestStatUtils(TestCase):

    def test_missing_leagues(self):
        with self.assertRaises(ValueError):
            get_stat_from_stat_list('R', [StatResult('7', 50)], league_type='nfl')
        with self.assertRaises(ValueError):
            get_stat_and_value(StatResult('7', 50), league_type='nfl')

    def test_get_stat_and_value(self):
        # String stat ID and stat value
        self.assertEqual(
            get_stat_and_value(StatResult('60', '65/290')),
            ('H/AB', '65/290'),
        )
        # Integer stat ID and stat value
        self.assertEqual(
            get_stat_and_value(StatResult(7, 50)),
            ('R', 50),
        )

    def test_get_stat_from_stat_list(self):
        stat_list = [
            StatResult('60', '65/290'),  # H/AB
            StatResult('7', 50),  # Hitter Runs
            StatResult('36', 10),  # Pitcher Runs
        ]
        self.assertEqual(get_stat_from_stat_list('H/AB', stat_list), '65/290')
        # Make sure we can get hitter runs and pitcher runs with our order flag
        self.assertEqual(get_stat_from_stat_list('R', stat_list, order=1), 50)
        self.assertEqual(get_stat_from_stat_list('R', stat_list, order=0), 10)
        # Stat missing from stat list
        with self.assertRaises(ValueError):
            get_stat_from_stat_list('HR', stat_list)
        # Non existent stat
        with self.assertRaises(ValueError):
            get_stat_from_stat_list('WAR++', stat_list)