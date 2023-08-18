def fill_db(db, models):
    flashcard = models.question(question="Lesson_1 - Question_1",
                                answer='Lesson_1 - Answer_1',
                                lesson=1)
    db.session.add(flashcard)

    flashcard = models.question(question="Lesson_1 - Question_2",
                                answer='Lesson_1 - Answer_2',
                                lesson=1)
    db.session.add(flashcard)

    flashcard = models.question(question="Lesson_2 - Question_1",
                                answer='Lesson_2 - Answer_1',
                                lesson=2)
    db.session.add(flashcard)

    flashcard = models.question(question="Lesson_2 - Question_2",
                                answer='Lesson_2 - Answer_2',
                                lesson=2)
    db.session.add(flashcard)

    flashcard = models.question(question="Lesson_3 - Question_1",
                                answer='Lesson_3 - Answer_1',
                                lesson=3)
    db.session.add(flashcard)

    flashcard = models.question(question="Lesson_3 - Question_2",
                                answer='Lesson_3 - Answer_2',
                                lesson=3)
    db.session.add(flashcard)

    flashcard = models.question(question="Lesson_4 - Question_1",
                                answer='Lesson_4 - Answer_1',
                                lesson=4)
    db.session.add(flashcard)

    flashcard = models.question(question="Lesson_4 - Question_2",
                                answer='Lesson_4 - Answer_2',
                                lesson=4)
    db.session.add(flashcard)

    flashcard = models.question(question="Lesson_5 - Question_1",
                                answer='Lesson_5 - Answer_1',
                                lesson=5)
    db.session.add(flashcard)

    flashcard = models.question(question="Lesson_5 - Question_2",
                                answer='Lesson_5 - Answer_2',
                                lesson=5)
    db.session.add(flashcard)

    flashcard = models.question(question="Lesson_6 - Question_1",
                                answer='Lesson_6 - Answer_1',
                                lesson=6)
    db.session.add(flashcard)

    flashcard = models.question(question="Lesson_6 - Question_2",
                                answer='Lesson_6 - Answer_2',
                                lesson=6)
    db.session.add(flashcard)

    db.session.commit()