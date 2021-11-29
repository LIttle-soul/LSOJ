from app.models import Solution, Problem
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

def get_problem():
    solution = Solution.objects.all()
    problems = Problem.objects.all()
    for problem in problems:
        problem.problem_solved = solution.filter(problem_id=problem.problem_id, run_result=4).count()
        problem.problem_submit = solution.filter(problem_id=problem.problem_id).count()
        problem.save()
    print(datetime.now())

if __name__ =='__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(get_problem, 'interval', minutes=10)
    scheduler.start()
