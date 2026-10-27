import unittest
from fcfs_simulator import schedule_fcfs

class TestFCFS(unittest.TestCase):
    def test_sample(self):
        p = [{'id':'P1','arrival':0,'burst':5},{'id':'P2','arrival':1,'burst':3},
             {'id':'P3','arrival':2,'burst':8},{'id':'P4','arrival':3,'burst':2}]
        rows, timeline, avg = schedule_fcfs(p)
        self.assertEqual([r['completion'] for r in rows], [5,8,16,18])
        self.assertEqual([r['turnaround'] for r in rows], [5,7,14,15])
        self.assertEqual([r['waiting'] for r in rows], [0,4,6,13])
        self.assertEqual(avg, {'waiting':5.75,'turnaround':10.25})
    def test_idle_and_unsorted(self):
        p = [{'id':'P2','arrival':7,'burst':2},{'id':'P1','arrival':2,'burst':3}]
        rows, timeline, avg = schedule_fcfs(p)
        self.assertEqual([r['id'] for r in rows], ['P1','P2'])
        self.assertEqual([(s['label'],s['start'],s['end']) for s in timeline],
                         [('IDLE',0,2),('P1',2,5),('IDLE',5,7),('P2',7,9)])
        self.assertEqual([r['waiting'] for r in rows], [0,0])
    def test_equal_arrival_stable(self):
        p = [{'id':'A','arrival':0,'burst':3},{'id':'B','arrival':0,'burst':1}]
        rows, _, _ = schedule_fcfs(p)
        self.assertEqual([r['id'] for r in rows], ['A','B'])
    def test_invalid(self):
        for p in ([], [{'id':'P','arrival':-1,'burst':2}], [{'id':'P','arrival':0,'burst':0}]):
            with self.assertRaises(ValueError):
                schedule_fcfs(p)

if __name__ == '__main__':
    unittest.main()
