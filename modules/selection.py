"""Seclection module to handle search page selection options."""
import sqlite3
from typing import Any


class Option:
    """Option hold data about this connection and its connection."""

    def __init__(self, name: str, selection_type: str):
        """Seclection_type can be {institutions |faculties| lecturers|courses|years}."""
        self.name = name
        self.selection_type: str = selection_type
        self.connections: list["Option"] = list()

    def add_conections(self, *args: "Option") -> None:
        """Adding each of *args to connections."""
        for con in args:
            self.connections.append(con)


class Selections:
    """
    Creating and managing the connections btween Options.

    public:
    -- Selections (constructor)
    -- get_selections (method)
    """

    def __init__(self, db_name):
        """
        Create Selections.

        Object fields:
        -- name_translators : names into list of ids (many ids may have same name).
        -- options : dict of all that below:
        -- dictionaries with str(id) as keys and list of Options as vales
           each Option is name correspondingly
            -- institutions
            -- faculties
            -- lecturers
            -- years
            -- courses
        """
        tables: tuple[list[Any], ...] = self.__get_tables_from_db(db_name)
        id_translators: dict[str, dict[str, str]] = self.__init_id_translators(tables)
        self.name_translators: dict[
            str, dict[str, list[str]]
        ] = self.__init_name_translators(id_translators)
        (
            self.institutions,
            self.faculties,
            self.lecturers,
            self.years,
            self.courses,
        ) = self.__create_options(tables)
        self.options = {
            "institutions": self.institutions,
            "faculties": self.faculties,
            "lecturers": self.lecturers,
            "years": self.years,
            "courses": self.courses,
        }

    def __get_tables_from_db(self, db_name: str) -> tuple[list[Any], ...]:
        """Retriving tables from db ad lists."""
        with sqlite3.connect(db_name) as con:
            insti_cur: sqlite3.Cursor = con.execute("select * from Institutions")
            facul_cur: sqlite3.Cursor = con.execute("select * from Faculties")
            facin_cur: sqlite3.Cursor = con.execute("select * from FacIn")
            lectu_cur: sqlite3.Cursor = con.execute("select * from Lecturers")
            cours_cur: sqlite3.Cursor = con.execute("select * from Courses")
            return (
                insti_cur.fetchall(),
                facul_cur.fetchall(),
                facin_cur.fetchall(),
                lectu_cur.fetchall(),
                cours_cur.fetchall(),
            )

    def __init_id_translators(
        self, tables: tuple[list[Any], ...]
    ) -> dict[str, dict[str, str]]:
        """Create for each selection id translator."""
        (
            insti_table,
            facul_table,
            _,
            lectu_table,
            cours_table,
        ) = tables
        id_to_institution = dict(insti_table)
        id_to_faculty = dict(facul_table)
        id_to_lecturer = {ID: name for (ID, name, _, _) in lectu_table}
        id_to_course = {ID: name for (ID, name, _, _) in cours_table}
        return {
            "institutions": id_to_institution,
            "faculties": id_to_faculty,
            "lecturers": id_to_lecturer,
            "courses ": id_to_course,
        }

    def __init_name_translators(
        self, id_translators: dict[str, dict[str, str]]
    ) -> dict[str, dict[str, list[str]]]:
        """Create a reverse of id_translator to find ids related to name."""
        name_translators: dict[str, dict[str, list[str]]] = {}
        for key, id_translator in id_translators.items():
            name_translators[key] = dict()
            for id_, name in id_translator.items():
                if name not in id_translators[key].keys():
                    name_translators[key][name] = [str(id_)]
                else:
                    name_translators[key][name].append(str(id_))
        return name_translators

    def __create_options(
        self, tables: tuple[list[Any], ...]
    ) -> tuple[dict[str, Option], ...]:
        """Create all Options with all connections from given data."""
        (
            insti_table,
            facul_table,
            facin_table,
            lectu_table,
            cours_table,
        ) = tables
        ins_options: dict[str, Option] = self.__create_institution_options(insti_table)
        fac_options: dict[str, Option] = self.__create_faculties_options(facul_table)
        lecturers_options: dict[str, Option] = self.__create_lecturers_options(
            lectu_table
        )
        years_options: dict[str, Option] = self.__create_years_options(cours_table)
        courses_options: dict[str, Option] = self.__create_courses_options(cours_table)
        self.__connect_faculties_institutions_options(
            facin_table, fac_options, ins_options
        )
        self.__connect_lecturer_faculties_options(
            lectu_table, lecturers_options, fac_options
        )
        self.__connect_lecturer_courses_years_options(
            cours_table, lecturers_options, courses_options, years_options
        )
        return (
            ins_options,
            fac_options,
            lecturers_options,
            years_options,
            courses_options,
        )

    def __create_institution_options(self, insti_table: list[Any]) -> dict[str, Option]:
        """Build dict of id:Option of institutions options."""
        institutions_options = dict()
        for ins_id, name in insti_table:
            institutions_options[str(ins_id)] = Option(name, "institutions")
        return institutions_options

    def __create_faculties_options(self, facul_table: list[Any]) -> dict[str, Option]:
        """Build dict of id:Option of faculties options."""
        faculties_options = dict()
        for fac_id, name in facul_table:
            faculties_options[str(fac_id)] = Option(name, "faculties")
        return faculties_options

    def __create_lecturers_options(self, lectu_table: list[Any]) -> dict[str, Option]:
        """Build dict of id:Option of lecturers options."""
        lecturers_oprtions = dict()
        for lec_id, name, _, _ in lectu_table:
            lecturers_oprtions[str(lec_id)] = Option(name, "lecturers")
        return lecturers_oprtions

    def __create_years_options(self, cours_table: list[Any]) -> dict[str, Option]:
        """Build dict of id:Option of years options."""
        years_options: dict[str, Option] = dict()
        for _, _, _, year in cours_table:
            if str(year) not in years_options.keys():
                years_options[str(year)] = Option(str(year), "years")
        return years_options

    def __create_courses_options(self, cours_table: list[Any]) -> dict[str, Option]:
        """Build dict of id:Option of courses options."""
        courses_options = dict()
        for cor_id, name, _, _ in cours_table:
            courses_options[str(cor_id)] = Option(name, "courses")
        return courses_options

    def __connect_faculties_institutions_options(
        self,
        facin_table: list[Any],
        fac_options: dict[str, Option],
        ins_options: dict[str, Option],
    ) -> None:
        """Add conection from institutions to facilties."""
        for ins_id, fac_id in facin_table:
            ins_options[str(ins_id)].add_conections(fac_options[str(fac_id)])

    def __connect_lecturer_faculties_options(
        self,
        lectu_table: list[Any],
        lecturer_option: dict[str, Option],
        fac_options: dict[str, Option],
    ):
        """Add conections from faculties to lecturers."""
        for lec_id, _, fac_id, _ in lectu_table:
            fac_options[str(fac_id)].add_conections(lecturer_option[str(lec_id)])

    def __connect_lecturer_courses_years_options(
        self,
        cours_table: list[Any],
        lecturer_option: dict[str, Option],
        course_option: dict[str, Option],
        years_options: dict[str, Option],
    ):
        """
        Add two connections.

        Add conections from lecturers to courses
        and add conections from years to courses.
        """
        for cor_id, _, lec_id, year in cours_table:
            lecturer_option[str(lec_id)].add_conections(course_option[str(cor_id)])
            years_options[str(year)].add_conections(course_option[str(cor_id)])

    def get_selections(self, **kwargs: str) -> dict[str, tuple[str, ...]]:
        """
        Receive current selection status and returning corresponding selection.

        For update next selection acurding to that selected in kwargs
        """
        (
            institutions_selected,
            faculties_selected,
            lecturers_selected,
            courses_selected,
            years_selected,
        ) = self.__get_selection_status(kwargs)
        institutions = set(self.institutions.values())
        faculties = set()
        lecturers = set()
        courses = set()
        years = set(self.years.values())

        if institutions_selected:
            selected_institution = kwargs["institutions"]
            faculties = self.__get_next_selection("institutions", selected_institution)

        if faculties_selected:
            selected_facultie = kwargs["faculties"]
            if selected_facultie in [o.name for o in faculties]:
                lecturers = self.__get_next_selection("faculties", selected_facultie)

        if lecturers_selected:
            selected_lecturer = kwargs["lecturers"]
            if selected_lecturer in [o.name for o in lecturers]:
                courses = self.__get_next_selection("lecturers", selected_lecturer)

        if courses_selected and not years_selected:
            for year in years:
                tmp = set(year.connections)
                if set.union(tmp, courses):
                    years.add(year)

        if courses_selected and years_selected:
            selected_year = str(kwargs["years"])
            courses2 = set()
            if selected_year in self.years.keys():
                courses2 = set(self.years[selected_year].connections)
            courses = set.intersection(courses, courses2)

        return self.__set_to_selection_dict(
            set.union(institutions, faculties, lecturers, courses, years)
        )

    def __get_selection_status(
        self, slections: dict[str, str]
    ) -> tuple[bool, bool, bool, bool, bool]:
        """Map given selection to where it is indeed seleced and where not."""
        return (
            "institutions" in slections.keys() and slections["institutions"] != "all",
            "faculties" in slections.keys() and slections["faculties"] != "all",
            "lecturers" in slections.keys() and slections["lecturers"] != "all",
            "courses" in slections.keys() and slections["courses"] != "all",
            "years" in slections.keys() and slections["years"] != "all",
        )

    def __get_next_selection(
        self, selection_type: str, current_selection: str
    ) -> set[Option]:
        """
        Retrive connections.

        connections with depth=1
        wwhere this name is <current_selection>
        and type <selection_type>.
        """
        options: set[Option] = set()
        if current_selection in self.name_translators[selection_type].keys():
            ids = self.name_translators[selection_type][current_selection]
            for id_ in ids:
                options = options.union(
                    set(self.options[selection_type][id_].connections)
                )

        return options

    def __set_to_selection_dict(
        self, option_set: set[Option]
    ) -> dict[str, tuple[str, ...]]:
        """
        Convert of Option JSON fienly format.

        Converting Options to sting and sorting
        years by number value
        rest by alphabetical order.
        """
        selections_dict_of_lists: dict[str, list[str]] = {
            "faculties": [],
            "institutions": [],
            "lecturers": [],
            "courses": [],
            "years": [],
        }
        for option in option_set:
            selections_dict_of_lists[option.selection_type].append(option.name)

        selections_dict_of_tuples: dict[str, tuple[str, ...]] = {}

        for sel, list_ in selections_dict_of_lists.items():
            list_ = list(set(list_))
            # sort alphabeticaly string and numericly years
            if sel == "years":
                list_.sort(key=lambda x: int(x))
            else:
                list_.sort(key=lambda x: x.lower())
            selections_dict_of_tuples[sel] = tuple(list_)
        return selections_dict_of_tuples
