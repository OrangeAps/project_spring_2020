from main import db
from time import sleep
from data.__all_models import Job, Player


def payday():
    players = db.query(Player).all()
    for player in players:
        job_id = player.job
        job = db.query(Job).filter(Job.id == job_id).first()
        player.money += job.wage
    db.commit()
    print('payday')


def main():
    while True:
        payday()
        sleep(3600.0)


if __name__ == '__main__':
    main()