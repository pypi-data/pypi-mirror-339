from pydantic import BaseModel, ConfigDict


class BaseConfig(BaseModel):
    model_config = ConfigDict(validate_assignment=True, extra="forbid")

    # to_dict and from_dict methods that allow for serialization and deserialization of the class
    def to_dict(self) -> dict:
        """
        Convert the BaseConfig object to a dictionary representation.

        Returns
        -------
        d :
            Dictionary representation of the BaseConfig object.
        """
        # Collect fields
        fields = {
            field_name: getattr(self, field_name)
            for field_name in self.model_fields.keys()
        }
        # Collect private attributes
        private_attributes = {
            private_attr_name: getattr(self, private_attr_name)
            for private_attr_name in self.__private_attributes__.keys()
        }
        return {
            "type": self.__class__.__name__,
            "fields": fields,
            "private_attributes": private_attributes,
        }

    @classmethod
    def from_dict(cls, d):
        """
        Instantiate a BaseConfig object from a dictionary.

        Parameters
        ----------
        d : dict
            Dictionary containing the fields required to instantiate the class.

        Returns
        -------
        obj :
            Instance of the class with the fields specified in the dictionary.
        """
        # Create an instance of the class with the fields specified in the dictionary
        obj = cls(**d["fields"])
        # Manually add the private attributes
        for private_attr_name, private_attr_value in d["private_attributes"].items():
            setattr(obj, private_attr_name, private_attr_value)
        return obj
