from random import randint
from typing import Tuple
from database_infrastructure_local.number_generator import NumberGenerator
from database_mysql_local.generic_crud import GenericCRUD
from email_address_local.email_address import EmailAddressesLocal
from location_local.locations_local_crud import LocationsLocal
from logger_local.MetaLogger import MetaLogger

from .constants import user_local_python_code_logger_object

# TODO Adding is_same_user() which override people.is_same_enity() checking username only


class UsersLocal(
    GenericCRUD, metaclass=MetaLogger, object=user_local_python_code_logger_object
):
    def __init__(self, is_test_data: bool = False):
        super().__init__(
            default_schema_name="user",
            default_view_table_name="user_not_deleted_view",
            default_table_name="user_table",
            default_column_name="user_id",
            is_test_data=is_test_data,
        )

    # When inserting a deleted entity (all entities except person and tables of codes i.e. country, state, county, city, neighbourhood, street ...) and table_definition.insert_is_undelete=false, we should null all the unique fields of the deleted entity- if_same_even_deleted_return_existing_id=true  # noqa
    def insert(
        self,
        *,
        username: str,
        main_email_address: str,  # noqa
        first_name: str,
        last_name: str,
        location_id: int,
        is_test_data: bool = False
    ) -> int:
        """Returns user_id (int) of the inserted user record"""
        number = NumberGenerator.get_random_number("user", "user_table", "user_id")
        # TODO develop GenericCRUD.__fix_data_dict() and then remove the `` from user.main_email_address
        data_dict = {
            "number": number,
            "username": username,
            "`user.main_email_address`": main_email_address,
            "first_name": first_name,
            "last_name": last_name,
            "active_location_id": location_id,
            "is_test_data": is_test_data,
        }
        user_id = super().insert(data_dict=data_dict)
        return user_id

    def update_by_user_id(
        self,
        user_id: int,
        username: str = None,
        main_email_address: str = None,
        first_name: str = None,
        last_name: str = None,
        active_location_id: int = None,
    ) -> int:
        """Updates the user record with the given user_id with the given values"""
        data_dict = {
            k: v
            for k, v in locals().items()
            if k not in ("__class__", "self") and v is not None
        }
        assert len(data_dict) > 1, "At least one of the fields must be updated"
        super().update_by_column_and_value(
            column_name="user_id", column_value=user_id, data_dict=data_dict
        )

    def read_user_tuple_by_user_id(
        self, user_id: int
    ) -> Tuple[int, int, str, str, str, str, int]:
        """
        Returns a tuple of (username, user.main_email_address, first_name, last_name, active_location_id)
        """
        user_tuple = self.select_one_tuple_by_column_and_value(
            select_clause_value=" username, `user.main_email_address`, first_name, last_name, active_location_id",
            column_value=user_id,
        )
        return user_tuple

    def read_user_dict_by_user_id(self, user_id: int) -> dict:
        """
        Returns a tuple of (number, username, user.main_email_address, first_name, last_name, active_location_id)
        """
        user_dict = self.select_one_dict_by_column_and_value(
            select_clause_value="number, username, `user.main_email_address`, first_name, last_name, active_location_id",
            column_value=user_id,
        )
        if not user_dict:
            user_dict = self.select_one_dict_by_column_and_value(
                view_table_name="user_to_be_reviewed_view",
                select_clause_value="number, username, `user.main_email_address`, first_name, last_name, active_location_id",
                column_value=user_id,
            )
        return user_dict

    def delete_by_user_id(self, user_id: int):
        """
        Updates the user end_timestamp with the given user_id
        """
        self.delete_by_column_and_value(id_column_value=user_id)

    def get_test_user_id(self):
        username = "test username " + str(randint(1, 100000))
        test_email_address = EmailAddressesLocal.get_test_email_address()
        first_name = "test first name " + str(randint(1, 100000))
        last_name = "test last name " + str(randint(1, 100000))
        test_location_id = LocationsLocal().get_test_location_id()
        insert_kwargs = {
            "username": username,
            "main_email_address": test_email_address,
            "first_name": first_name,
            "last_name": last_name,
            "location_id": test_location_id,
        }

        return_result = self.get_test_entity_id(
            entity_name="user", insert_function=self.insert, insert_kwargs=insert_kwargs
        )

        return return_result
