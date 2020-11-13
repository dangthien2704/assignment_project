from django.db import models
import assignments.models


class TakeAssignmentManager(models.Manager):
    def compute_grade(self, student, assignment, validated_data):
        """Getting the answers of questions from DB"""
        questions_of_assignment = assignment.questions_of_assignment.all()
        answer_of_assignment = [str(q.answer_of_question) for q in questions_of_assignment]
        # print ('MANAGER', assignment)

        """Getting the answers of student"""
        questions_of_assignment = validated_data['questions_of_assignment']
        final_answer = [q['answer_of_student']['answer_text'] for q in questions_of_assignment]
        # print ('FINAL ANSWER', final_answer)

        """Comparing answer of student&questions then calculate score"""
        result = 0
        for a, b in zip(final_answer, answer_of_assignment):
            if a == b:
                result += 1
        score = result / len(questions_of_assignment) * 10
        # print ('SCORE', score)

        """Calculating progress"""
        completed_question = 0
        for a in final_answer:
            if a != '':
                completed_question += 1
        progress = completed_question/len(questions_of_assignment)*100
        formatted_progress = "{}%".format(
            completed_question/len(questions_of_assignment)*100)
        # print ('PROGRESS', formatted_progress)

        """Checking if the assignment has been completed"""
        if progress < 100:
            completed = "False"
        else:
            completed = "True"
        # print ('completed', completed)

        return {
            'final_answer': final_answer,
            'progress': formatted_progress,
            'completed': completed,
            'grade': score
        }

    def create(self, student, assignment, validated_data):
        record = self.compute_grade(student, assignment, validated_data)
        final_answer = record.pop('final_answer')
        print('RECORD', record)
        # record_update = record.pop('assignment')

        """Creating instance in DB of GradedAssignment"""
        created_grade, created = assignments.models.GradedAssignment.objects.update_or_create(
            student=student,
            assignment=assignment,
            defaults={
                **record
            },
        )

        """Creating instance in DB of StudentAnswer"""
        created_studentanswer, created = assignments.models.StudentAnswer.objects.update_or_create(
            student=student,
            assignment=assignment,
            defaults={
                'answer_text': final_answer,
                **record
            },
        )

        return created_grade, created_studentanswer
