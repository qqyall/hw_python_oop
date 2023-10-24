from dataclasses import dataclass, asdict
from typing import List
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE_TEMPLATE: str = (
        "Тип тренировки: {training_type}; "
        "Длительность: {duration:.3f} ч.; "
        "Дистанция: {distance:.3f} км; "
        "Ср. скорость: {speed:.3f} км/ч; "
        "Потрачено ккал: {calories:.3f}."
    )

    def get_message(self) -> str:
        return self.MESSAGE_TEMPLATE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ):
        self.action = action
        self.duration = duration
        self.weight = weight

    MINS_IN_HOUR: int = 60
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения км/ч."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError()

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


@dataclass
class Running(Training):
    """Тренировка: бег."""
    action: int = 0
    duration: float = 0.
    weight: float = 0.

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        return (
            (self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
             + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight / self.M_IN_KM
            * self.duration * self.MINS_IN_HOUR
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    action: int = 0
    duration: float = 0.
    weight: float = 0.
    height: int = 0

    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_MULTIPLIER: float = 0.029
    COEF_KMH_TO_MS: float = 0.278
    SM_IN_METR: int = 100

    def get_spent_calories(self) -> float:
        mean_speed_ms: float = self.get_mean_speed() * self.COEF_KMH_TO_MS
        height_m: float = self.height / self.SM_IN_METR

        return (
            (self.CALORIES_WEIGHT_MULTIPLIER * self.weight
             + (mean_speed_ms**2 / height_m) * self.CALORIES_SPEED_MULTIPLIER
             * self.weight) * self.duration * self.MINS_IN_HOUR
        )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    action: int = 0
    duration: float = 0.
    weight: float = 0.
    length_pool: int = 0
    count_pool: int = 0

    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 2
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1

    def get_mean_speed(self) -> float:
        return (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        return (
            (self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.CALORIES_MEAN_SPEED_MULTIPLIER * self.weight * self.duration
        )


def read_package(workout_type: str, data: List[int | float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_types: Dict[str, Type[Training]] = {
        "SWM": Swimming,
        "RUN": Running,
        "WLK": SportsWalking
    }
    if workout_type not in workout_type:
        raise ValueError("Упражнение не найдено")
    return workout_types[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == "__main__":
    packages = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
