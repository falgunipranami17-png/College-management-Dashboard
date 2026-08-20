from flask import Flask, render_template, request, redirect, url_for

from main import (
    Base,
    SessionLocal,
    Branch,
    Student,
    Profile,
    Club
)

session = SessionLocal()

app = Flask(__name__)


# HOME PAGE

@app.route("/")
def index():

    students = session.query(Student).all()
    branches = session.query(Branch).all()
    clubs = session.query(Club).all()

    return render_template(
        "index.html",
        students=students,
        branches=branches,
        clubs=clubs
    )


# ADD BRANCH / CLUB

@app.route("/add_branch_club", methods=["POST"])
def add_branch_club():

    branch_name = request.form.get("branch_name")
    club_name = request.form.get("club_name")

    # Add Branch
    if branch_name:

        existing_branch = session.query(Branch).filter_by(
            name=branch_name
        ).first()

        if not existing_branch:

            new_branch = Branch(name=branch_name)

            session.add(new_branch)


    # Add Club
    if club_name:

        existing_club = session.query(Club).filter_by(
            name=club_name
        ).first()

        if not existing_club:

            new_club = Club(name=club_name)

            session.add(new_club)


    session.commit()

    return redirect(url_for("index"))


# DELETE BRANCH

@app.route("/delete_branch/<int:id>", methods=["GET"])
def delete_branch(id):

    branch = session.query(Branch).get(id)

    if branch:

        session.delete(branch)
        session.commit()

    return redirect(url_for("index"))


# DELETE CLUB

@app.route("/delete_club/<int:id>", methods=["GET"])
def delete_club(id):

    club = session.query(Club).get(id)

    if club:

        session.delete(club)
        session.commit()

    return redirect(url_for("index"))


# ADD STUDENT

@app.route("/add_student", methods=["POST"])
def add_student():

    name = request.form.get("name")
    bio = request.form.get("bio")
    branch_id = request.form.get("branch_id")

    student = Student(name=name)

    if branch_id:

        student.branch_id = int(branch_id)

    profile = Profile(
        bio=bio,
        student=student
    )

    session.add(student)
    session.add(profile)

    session.commit()

    return redirect(url_for("index"))


# ASSIGN BRANCH / CLUB

@app.route("/assign_club_branch", methods=["POST"])
def assign_club_branch():

    student_id = int(request.form["student_id"])

    branch_id = request.form.get("branch_id")

    club_ids = request.form.getlist("club_ids")

    student = session.query(Student).get(student_id)

    if student:

        # Assign branch
        if branch_id:

            student.branch_id = int(branch_id)

        # Assign clubs
        for club_id in club_ids:

            club = session.query(Club).get(
                int(club_id)
            )

            if club and club not in student.clubs:

                student.clubs.append(club)

        session.commit()

    return redirect(url_for("index"))

# REMOVE BRANCH

@app.route("/remove_branch/<int:student_id>", methods=["GET"])
def remove_branch(student_id):

    student = session.query(Student).get(student_id)

    if student:

        student.branch_id = None

        session.commit()

    return redirect(url_for("index"))


# REMOVE CLUB

@app.route(
    "/remove_club/<int:student_id>/<int:club_id>",
    methods=["GET"]
)
def remove_club(student_id, club_id):

    student = session.query(Student).get(student_id)

    club = session.query(Club).get(club_id)

    if student and club and club in student.clubs:

        student.clubs.remove(club)

        session.commit()

    return redirect(url_for("index"))


# DELETE STUDENT

@app.route("/delete_student/<int:id>", methods=["GET"])
def delete_student(id):

    student = session.query(Student).get(id)

    if student:

        session.delete(student)

        session.commit()

    return redirect(url_for("index"))

# RUN APPLICATION

if __name__ == "__main__":
    app.run(debug=True)