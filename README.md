# Language Learning App

## DB Models
### User
id: PK
email: str (email format, max: 256)
background: str (HEX format)
emoji: str (max: 24)
password: str (password hash)
streak: int (min: 0)

### Lesson
id: PK
name: str (max: 1024)
content: str
order: int (unique, starts with 0)

### Progress
user_id: FK to User.id
lesson_id: FK to Lesson.id

### Exercise
id: PK
lesson_id: FK to Lesson.id
type: Enum(audio/photo/multiple-choice/free)
definition: str (max: 512)
link: str (max: 512)
option_a: str (only for multiple-choice type)
option_b: str (only for multiple-choice type)
option_c: str (only for multiple-choice type)
option_d: str (only for multiple-choice type)
answers: str (max: 2048)
