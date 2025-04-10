from dataclasses import dataclass
from pprint import pprint

from ovld import Medley, call_next, ovld, recurse

from serieux import Context, Serieux, deserialize
from serieux.partial import Sources

##################
# Implementation #
##################


@Serieux.extend
class Dotted(Medley):
    @ovld(priority=10)
    def deserialize(self, t: type[object], obj: dict, ctx: Context):
        if any("." in k for k in obj.keys()):
            parts = []
            for k, v in obj.items():
                levels = k.split(".")
                current = v
                while levels:
                    current = {levels.pop(): current}
                parts.append(current)
            return recurse(t, Sources(*parts), ctx)
        return call_next(t, obj, ctx)


#################
# Demonstration #
#################


@dataclass
class Climate:
    hot: bool
    sunny: bool


@dataclass
class City:
    name: str
    population: int
    climate: Climate


@dataclass
class Country:
    name: str
    capital: City


def main():
    data = {
        "name": "Canada",
        "capital": {
            "name": "Ottawa",
        },
        "capital.population": 800_000,
        "capital.climate.hot": False,
        "capital.climate.sunny": False,
    }
    deser = deserialize(Country, data)
    pprint(deser)
    assert deser == Country(
        name="Canada",
        capital=City(
            name="Ottawa",
            population=800_000,
            climate=Climate(
                hot=False,
                sunny=False,
            ),
        ),
    )


if __name__ == "__main__":
    main()
