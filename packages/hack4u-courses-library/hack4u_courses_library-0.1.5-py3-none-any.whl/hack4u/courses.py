class Course:
    def __init__(self, name: str, duration: int, link: str):
        self.name = name
        self.duration = duration
        self.link = link

    # Representacion de clase
    def __repr__(self):
        return f"{self.name} [{self.duration} horas] ({self.link})"


courses = [
    Course("Introduccion a linux", 15, "https://course.com/linux/"),
    Course("Personalizacion de linux", 3, "https://course.com/personalisacion"),
    Course("Introduccion al hacking", 54, "https://course.com/intro-hacking"),
]


def list_courses():
    for course in courses:
        print(course)


def find_course_name(name):
    for course in courses:
        course_name = course.name.lower()
        if course_name == name:
            return course
    return "Curso no encontrado"
