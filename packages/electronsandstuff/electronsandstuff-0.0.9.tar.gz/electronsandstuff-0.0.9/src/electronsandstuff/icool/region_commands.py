from pydantic import Field
from typing import List, Union, Literal, Tuple, Annotated, Optional
import logging

from .base import ICoolBase
from .substitution import (
    FloatOrSub,
    StrOrSub,
    IntOrSub,
    BoolOrSub,
    to_bool_or_sub,
    to_float_or_sub,
    to_int_or_sub,
    to_str_or_sub,
)
from .fields import all_fields, ICoolField
from .geometry import all_geometry, ICoolGeometry
from .utils import stripped_no_comment_str


logger = logging.getLogger(__name__)


class RegionCommand(ICoolBase):
    pass

    def expand(self) -> List["RegionCommand"]:
        """
        Expand this command by resolving all repetitions.

        Returns
        -------
        List[RegionCommand]
            A list of RegionCommands
        """
        return [self.model_copy(deep=True)]

    def get_length(self, check_substitutions: bool = True) -> float:
        """
        Calculate the length of this region command.

        Parameters
        ----------
        check_substitutions : bool, default=True
            If True, verify that all substitutions have been made
            before calculating the length.

        Returns
        -------
        float
            The length of the region in meters. Base implementation returns 0.
        """
        if check_substitutions:
            self.assert_no_substitutions()
        return 0.0

    @classmethod
    def parse_input_file(
        cls, lines: List[str], start_idx: int, state: Optional[dict] = None
    ) -> Tuple["RegionCommand", int]:
        raise NotImplementedError


class RSubRegion(ICoolBase):
    rlow: FloatOrSub
    rhigh: FloatOrSub
    field: Annotated[all_fields, Field(discriminator="name")]
    mtag: StrOrSub
    geometry: Annotated[all_geometry, Field(discriminator="name")]


class SRegion(RegionCommand):
    name: Literal["SREGION"] = "SREGION"
    slen: FloatOrSub
    zstep: FloatOrSub
    subregions: List[RSubRegion]

    def get_length(self, check_substitutions: bool = True) -> float:
        """
        Calculate the length of this SRegion.

        Parameters
        ----------
        check_substitutions : bool, default=True
            If True, verify that all substitutions have been made
            before calculating the length.

        Returns
        -------
        float
            The length of the region in meters (slen value).
        """
        if check_substitutions:
            self.assert_no_substitutions()
        return self.slen

    @classmethod
    def parse_input_file(
        cls, lines: List[str], start_idx: int, state: Optional[dict] = None
    ) -> Tuple["RegionCommand", int]:
        slen, nrreg, zstep = stripped_no_comment_str(lines[start_idx + 1]).split()
        slen = to_float_or_sub(slen)
        zstep = to_float_or_sub(zstep)

        subregions = []
        end_idx = start_idx + 2
        for reg_idx in range(int(nrreg)):
            irreg, rlow, rhigh = stripped_no_comment_str(
                lines[start_idx + 2 + 6 * reg_idx]
            ).split()
            if int(irreg) != (reg_idx + 1):
                raise ValueError(
                    f"r region index did not match loop index. Something went wrong? (irreg={irreg}, loop_idx={reg_idx})"
                )

            field, _ = ICoolField.parse_input_file(lines, start_idx + 3 + 6 * reg_idx)
            mtag = stripped_no_comment_str(lines[start_idx + 5 + 6 * reg_idx])
            geometry, _ = ICoolGeometry.parse_input_file(
                lines, start_idx + 6 + 6 * reg_idx
            )
            subregions.append(
                RSubRegion(
                    rlow=to_float_or_sub(rlow),
                    rhigh=to_float_or_sub(rhigh),
                    field=field,
                    mtag=to_str_or_sub(mtag),
                    geometry=geometry,
                )
            )

            end_idx += 6
            logger.debug(
                f'Finished subregion {reg_idx} (end_idx={end_idx}, end_line="{lines[end_idx]}")'
            )

        obj = cls(
            slen=slen,
            zstep=zstep,
            subregions=subregions,
        )
        return obj, end_idx


# Phase models for "RefP"
class PhModRef2(ICoolBase):
    name: Literal["PHMODREF2"] = "PHMODREF2"


class PhModRef3(ICoolBase):
    name: Literal["PHMODREF3"] = "PHMODREF3"
    pz0: FloatOrSub
    t0: FloatOrSub


class PhModRef4(ICoolBase):
    name: Literal["PHMODREF4"] = "PHMODREF4"
    pz0: FloatOrSub
    t0: FloatOrSub
    dedz: FloatOrSub


class PhModRef5(ICoolBase):
    name: Literal["PHMODREF5"] = "PHMODREF5"
    e0: FloatOrSub
    dedz: FloatOrSub
    d2edz2: FloatOrSub


class PhModRef6(ICoolBase):
    name: Literal["PHMODREF6"] = "PHMODREF6"
    e0: FloatOrSub
    dedz: FloatOrSub
    d2edz2: FloatOrSub


class RefP(RegionCommand):
    name: Literal["REFP"] = "REFP"
    refpar: IntOrSub
    phmodref: Annotated[
        Union[PhModRef2, PhModRef3, PhModRef4, PhModRef5, PhModRef6],
        Field(discriminator="name"),
    ]

    @classmethod
    def parse_input_file(
        cls, lines: List[str], start_idx: int, state: Optional[dict] = None
    ) -> Tuple["RegionCommand", int]:
        # Pull out parameters
        refpar, param_a, param_b, param_c, phmoderef = stripped_no_comment_str(
            lines[start_idx + 1]
        ).split()
        refpar = to_int_or_sub(refpar)
        param_a = to_float_or_sub(param_a)
        param_b = to_float_or_sub(param_b)
        param_c = to_float_or_sub(param_c)

        # Generate the correct chlid class
        phmoderef_idx = int(phmoderef)
        if phmoderef_idx == 2:
            phmodref = PhModRef2()
        elif phmoderef_idx == 3:
            phmodref = PhModRef3(pz0=param_a, t0=param_b)
        elif phmoderef_idx == 4:
            phmodref = PhModRef4(pz0=param_a, t0=param_b, dedz=param_c)
        elif phmoderef_idx == 5:
            phmodref = PhModRef5(e0=param_a, dedz=param_b, d2edz2=param_c)
        elif phmoderef_idx == 6:
            phmodref = PhModRef6(e0=param_a, dedz=param_b, d2edz2=param_c)
        else:
            raise ValueError(f"Unrecognized PHMODREF: {phmoderef_idx}")
        return cls(refpar=refpar, phmodref=phmodref), (start_idx + 2)


class Ref2(RefP):
    name: Literal["REF2"] = "REF2"

    @classmethod
    def parse_input_file(
        cls, lines: List[str], start_idx: int, state: Optional[dict] = None
    ) -> Tuple["RegionCommand", int]:
        if state and "REFP" in state:
            lines = [
                lines[start_idx],
                f"{lines[start_idx+1]} {state['REFP'].phmodref.__class__.__name__[-1]}",
            ]
            obj, idx = super().parse_input_file(lines, 0, state)
            return obj, idx + start_idx
        else:
            raise ValueError(
                f"Found REF2 without seeing REFP first, cannot determine PHMODREF (contents of state dict: {state.keys() if state else state})"
            )


class Grid(RegionCommand):
    name: Literal["GRID"] = "GRID"
    grid_num: IntOrSub
    field_type: StrOrSub
    file_num: IntOrSub
    curvature_flag: IntOrSub
    ref_momentum: FloatOrSub
    field_scale: FloatOrSub
    curvature_sign: FloatOrSub
    file_format: IntOrSub
    long_shift: FloatOrSub

    @classmethod
    def parse_input_file(
        cls, lines: List[str], start_idx: int, state: Optional[dict] = None
    ) -> Tuple["RegionCommand", int]:
        grid_num = stripped_no_comment_str(lines[start_idx + 1])
        field_type = stripped_no_comment_str(lines[start_idx + 2])

        # Extract 15 grid parameters
        (
            _,
            file_num,
            curvature_flag,
            ref_momentum,
            field_scale,
            _,
            _,
            curvature_sign,
            file_format,
            long_shift,
            _,
            _,
            _,
            _,
            _,
        ) = stripped_no_comment_str(lines[start_idx + 3]).split()

        # Construct object
        obj = Grid(
            grid_num=to_int_or_sub(grid_num),
            field_type=to_str_or_sub(field_type),
            file_num=to_int_or_sub(file_num.rstrip(".")),
            curvature_flag=to_int_or_sub(curvature_flag.rstrip(".")),
            ref_momentum=to_float_or_sub(ref_momentum),
            field_scale=to_float_or_sub(field_scale),
            curvature_sign=to_float_or_sub(curvature_sign),
            file_format=to_int_or_sub(file_format.rstrip(".")),
            long_shift=to_float_or_sub(long_shift),
        )
        return obj, (start_idx + 4)


class DVar(RegionCommand):
    name: Literal["DVAR"] = "DVAR"
    var_idx: IntOrSub
    change: FloatOrSub
    apply_to: IntOrSub

    @classmethod
    def parse_input_file(
        cls, lines: List[str], start_idx: int, state: Optional[dict] = None
    ) -> Tuple["RegionCommand", int]:
        # Grab the parameters
        var_idx, change, apply_to = stripped_no_comment_str(
            lines[start_idx + 1]
        ).split()
        obj = cls(
            var_idx=to_int_or_sub(var_idx),
            change=to_float_or_sub(change),
            apply_to=to_int_or_sub(apply_to),
        )
        return obj, (start_idx + 2)


class Cell(RegionCommand):
    name: Literal["CELL"] = "CELL"
    n_cells: IntOrSub
    cell_flip: BoolOrSub
    field: Annotated[all_fields, Field(discriminator="name")]
    commands: List[
        Annotated[
            Union[SRegion, RefP, Ref2, Grid, DVar, "Repeat"],
            Field(discriminator="name"),
        ]
    ] = Field(default_factory=list)

    def expand(self) -> List[RegionCommand]:
        """
        Expand this cell by repeating its commands n_cells times and recursively
        expanding any nested commands.

        Returns
        -------
        List[RegionCommand]
            A list of expanded commands
        """
        # First expand all child commands
        expanded_commands = []
        for cmd in self.commands:
            expanded_commands.extend(cmd.expand())

        # Now repeat the expanded commands n_cells times
        result = []
        for _ in range(self.n_cells):
            result.extend([cmd.model_copy(deep=True) for cmd in expanded_commands])

        return result

    def get_length(self, check_substitutions: bool = True) -> float:
        """
        Calculate the length of this Cell, which is the sum of all contained commands
        multiplied by the number of cells.

        Parameters
        ----------
        check_substitutions : bool, default=True
            If True, verify that all substitutions have been made
            before calculating the length.

        Returns
        -------
        float
            The total length of the cell in meters.
        """
        if check_substitutions:
            self.assert_no_substitutions()

        # Sum up the lengths of all commands
        total_length = sum(
            cmd.get_length(check_substitutions=False) for cmd in self.commands
        )

        # Multiply by the number of cells
        return self.n_cells * total_length

    @classmethod
    def parse_input_file(
        cls, lines: List[str], start_idx: int, state: Optional[dict] = None
    ) -> Tuple["RegionCommand", int]:
        # Grab parameters from top of cell
        n_cells = to_int_or_sub(stripped_no_comment_str(lines[start_idx + 1]))
        cell_flip = to_bool_or_sub(stripped_no_comment_str(lines[start_idx + 2]))
        field, _ = ICoolField.parse_input_file(lines, start_idx + 3)

        # Process internal commands
        cmds, end_idx = parse_region_cmds(
            lines, start_idx + 5, end_cmd="ENDCELL", state=state
        )

        # Make object
        obj = cls(commands=cmds, n_cells=n_cells, cell_flip=cell_flip, field=field)
        return obj, end_idx


class Repeat(RegionCommand):
    name: Literal["REPEAT"] = "REPEAT"
    n_repeat: IntOrSub
    commands: List[
        Annotated[
            Union[SRegion, RefP, Ref2, Grid, DVar, "Repeat"],
            Field(discriminator="name"),
        ]
    ] = Field(default_factory=list)

    def expand(self) -> List[RegionCommand]:
        """
        Expand this repeat by repeating its commands n_repeat times and recursively
        expanding any nested commands.

        Returns
        -------
        List[RegionCommand]
            A list of expanded commands
        """
        # First expand all child commands
        expanded_commands = []
        for cmd in self.commands:
            expanded_commands.extend(cmd.expand())

        # Now repeat the expanded commands n_repeat times
        result = []
        for _ in range(self.n_repeat):
            result.extend([cmd.model_copy(deep=True) for cmd in expanded_commands])

        return result

    def get_length(self, check_substitutions: bool = True) -> float:
        """
        Calculate the length of this Repeat, which is the sum of all contained commands
        multiplied by the number of repeats.

        Parameters
        ----------
        check_substitutions : bool, default=True
            If True, verify that all substitutions have been made
            before calculating the length.

        Returns
        -------
        float
            The total length of the repeated section in meters.
        """
        if check_substitutions:
            self.assert_no_substitutions()

        # Sum up the lengths of all commands
        total_length = sum(
            cmd.get_length(check_substitutions=False) for cmd in self.commands
        )

        # Multiply by the number of repeats
        return self.n_repeat * total_length

    @classmethod
    def parse_input_file(
        cls, lines: List[str], start_idx: int, state: Optional[dict] = None
    ) -> Tuple["RegionCommand", int]:
        # Get the number of repeats
        n_repeat = to_int_or_sub(stripped_no_comment_str(lines[start_idx + 1]))

        # Process commands in the block
        cmds, end_idx = parse_region_cmds(
            lines, start_idx + 2, end_cmd="ENDR", state=state
        )

        # Return the object
        return cls(commands=cmds, n_repeat=n_repeat), end_idx


def parse_region_cmds(lines, start_idx, end_cmd="", state: Optional[dict] = None):
    if state is None:
        state = {}

    logger.debug(
        f"Begining to parse region commands (len(lines)={len(lines)}, start_idx={start_idx}, end_cmd={end_cmd})"
    )
    idx = start_idx
    cmds = []
    while idx < len(lines):
        cmd_name = stripped_no_comment_str(lines[idx])

        if not cmd_name:
            idx += 1
            continue

        # If we see a registered command, parse it and add to list
        if cmd_name == "SREGION":
            cmd, idx = SRegion.parse_input_file(lines, idx, state=state)
        elif cmd_name == "REFP":
            cmd, idx = RefP.parse_input_file(lines, idx, state=state)
            state["REFP"] = cmd
        elif cmd_name == "REF2":
            cmd, idx = Ref2.parse_input_file(lines, idx, state=state)
        elif cmd_name == "GRID":
            cmd, idx = Grid.parse_input_file(lines, idx, state=state)
        elif cmd_name == "DVAR":
            cmd, idx = DVar.parse_input_file(lines, idx, state=state)
        elif cmd_name == "CELL":
            cmd, idx = Cell.parse_input_file(lines, idx, state=state)
        elif cmd_name == "REPEAT":
            cmd, idx = Repeat.parse_input_file(lines, idx, state=state)
        elif cmd_name == end_cmd:
            logger.debug(f"Hit end command: {end_cmd}")
            idx += 1
            break
        else:
            logger.warning(f'Unrecognized command: "{cmd_name}"')
            idx += 1
            continue
        cmds.append(cmd)

    return cmds, idx


class CoolingSection(RegionCommand):
    """
    Represents the cooling section of an ICOOL input file.
    """

    name: Literal["SECTION"] = "SECTION"
    commands: List[
        Annotated[
            Union[SRegion, RefP, Ref2, Grid, DVar, Cell, Repeat],
            Field(discriminator="name"),
        ]
    ] = Field(default_factory=list, description="Content of the cooling section")

    def expand(self) -> List[RegionCommand]:
        """
        Expand this cooling section by expanding all commands within it.

        Returns
        -------
        List[RegionCommand]
            A list of expanded commands
        """
        expanded_commands = []
        for cmd in self.commands:
            expanded_commands.extend(cmd.expand())

        return expanded_commands

    def get_length(self, check_substitutions: bool = True) -> float:
        """
        Calculate the total length of the cooling section, which is the sum of all
        contained commands.

        Parameters
        ----------
        check_substitutions : bool, default=True
            If True, verify that all substitutions have been made
            before calculating the length.

        Returns
        -------
        float
            The total length of the cooling section in meters.
        """
        if check_substitutions:
            self.assert_no_substitutions()

        # Sum up the lengths of all commands
        return sum(cmd.get_length(check_substitutions=False) for cmd in self.commands)

    @classmethod
    def parse_input_file(
        cls, lines: List[str], start_idx: int
    ) -> Tuple["CoolingSection", int]:
        # Process commands in the block
        cmds, end_idx = parse_region_cmds(lines, start_idx + 1, end_cmd="ENDSECTION")

        # Return the object
        return cls(commands=cmds), end_idx
        cmds, end_idx = parse_region_cmds(lines, start_idx + 1, end_cmd="ENDSECTION")

        # Return the object
        return cls(commands=cmds), end_idx
