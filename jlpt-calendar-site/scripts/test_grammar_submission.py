import json
import sqlite3
import unittest
from pull_submissions import submission_details, insert_grammar_attempts


class GrammarSubmissionTests(unittest.TestCase):
    def test_v2_preserves_unknown_unanswered_and_payload(self):
        payload = {'unknownCount': 1, 'unansweredCount': 1, 'details': {
            'test_id': 'n2-grammar-speedrun-v2', 'memory_timing': 'guided_practice',
            'attempts': [{'item_no': 1, 'status': 'unknown', 'selected_text': '分からない', 'correct_text': 'つつある', 'response_seconds': 3},
                         {'item_no': 2, 'status': 'unanswered', 'selected_text': None, 'correct_text': 'ようにしている', 'response_seconds': 0}]}}
        d = submission_details({'payload_json': json.dumps(payload)})
        self.assertEqual((d['unknown'], d['unanswered'], d['guided']), (1, 1, True))
        self.assertEqual(json.loads(d['notes'])['submitted_result'], payload)
        c = sqlite3.connect(':memory:')
        c.execute('CREATE TABLE question_attempts(test_id, item_no, item_type_id, level_label, response_state, response_seconds, selected_text, correct_text)')
        insert_grammar_attempts(c.cursor(), 'fixture', d['attempts'])
        self.assertEqual(c.execute('SELECT response_state,selected_text,response_seconds FROM question_attempts ORDER BY item_no').fetchall(), [('unknown', '分からない', 3), ('unanswered', None, 0)])

    def test_legacy_does_not_invent_attempts(self):
        d = submission_details({'payload_json': '{}'})
        self.assertEqual((d['unknown'], d['unanswered'], d['attempts']), (0, 0, []))

    def test_partial_unused_pool_does_not_become_graded_attempts(self):
        payload = {'totalQuestions': 3, 'answeredQuestions': 3, 'plannedQuestions': 200,
                   'unattemptedCount': 197, 'unknownCount': 1, 'unansweredCount': 0,
                   'details': {'test_id': 'n2-grammar-speedrun-v2', 'scoring_version': 'answered-v1',
                               'termination_reason': 'early', 'memory_timing': 'guided_practice',
                               'unattempted_questions': [{'item_no': i, 'status': 'unattempted'} for i in range(4, 201)],
                               'attempts': [{'item_no': 1, 'status': 'correct'},
                                            {'item_no': 2, 'status': 'wrong'},
                                            {'item_no': 3, 'status': 'unknown'}]}}
        d = submission_details({'payload_json': json.dumps(payload)})
        self.assertEqual((d['unknown'], d['unanswered'], len(d['attempts'])), (1, 0, 3))
        self.assertEqual(json.loads(d['notes'])['submitted_result']['unattemptedCount'], 197)
        c = sqlite3.connect(':memory:')
        c.execute('CREATE TABLE question_attempts(test_id, item_no, item_type_id, level_label, response_state, response_seconds, selected_text, correct_text)')
        insert_grammar_attempts(c.cursor(), 'partial-fixture', d['attempts'])
        self.assertEqual(c.execute('SELECT COUNT(*) FROM question_attempts').fetchone()[0], 3)

    def test_bad_optional_payload_is_safe(self):
        self.assertEqual(submission_details({'payload_json': 'not json'})['attempts'], [])


if __name__ == '__main__':
    unittest.main()
