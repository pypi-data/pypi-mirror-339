"""Interactive conversion of magnetic units at the command line."""

from convmag import __version__
from convmag import convmag_functions as cm


def cli():
    """Interactive conversion of units at the command line."""
    CONVERTING = True
    msg1 = (
        f"convmag {__version__}\n\n"
        "***** Conversion between magnetic units. *****\n"
        "\nAt the 'Input:' promt, enter:\n"
        "[value startunit endunit] e.g. 6 T A/m,\n"
        "[units] to list the available units,\n"
        "[conv] to list the conversion factors or\n"
        "[q or Enter] to quit.\n"
    )
    print(msg1)
    while CONVERTING:
        r = input("\nInput: ")
        if r in ("q", ""):
            CONVERTING = False
        elif r == "units":
            uts = cm.units.copy()
            uts.add("muB/fu")
            u_s = "\n".join(sorted(uts, key=str.casefold))
            p_s = "\n".join(cm.prefactors)
            msg2 = (
                "\nThe base units available for conversion are:\n"
                f"{u_s}"
                "\n\nThe prefactors available for any base unit are:\n"
                f"{p_s}"
            )
            print(msg2)
        elif r == "conv":
            lgst = max(map(len, cm.units))
            print("\nThe conversions between base units available are:\n")
            for k in list(cm.convmag.keys()):
                St, En = k.split("_")
                print(f"{St:>{lgst}}  <->  {En:<{lgst}}:    {cm.convmag[k]}")
            p_sl = ", ".join(cm.prefactors)
            msg3 = (
                f"{'muB/fu':>{lgst}}  <->  {'T':<{lgst}}:    requires user input"
                "\n\nINFO: the factors given above are for the forward conversion"
                "\nINFO: permeability of free space, MU_0 = 4 * 3.14159 "
                "* 1e-7 H/m (== Vs/Am)\n"
                "INFO: Bohr magneton, MU_B =  9.274015e-24 Am^2"
                "\t(muB is the unit string for conversions with Bohr magnetons)\n"
                "INFO: prefactors available for any base unit: "
                f"{p_sl}"
                "\nINFO: emu is always defined as erg/G in this program"
            )
            print(msg3)

        elif r.count(" ") == 2:
            val = float(r.split(" ")[0])
            startunit = r.split(" ")[1]
            endunit = r.split(" ")[2]
            if "muB/fu" in [startunit, endunit] and "T" in [startunit, endunit]:
                msg4 = (
                    "\n***INFO: muB per formula unit <-> T***\n"
                    "Please enter lattice parameters: a b c in Angstrom\n"
                )
                print(msg4)
                lp = input("a b c: ")
                a = float(lp.split(" ")[0])
                b = float(lp.split(" ")[1])
                c = float(lp.split(" ")[2])
                print("\nLimited to orthogonal or hexagonal unit cells:")
                gamma_in = input("Please enter gamma in deg. (90 or 120): ")
                vol = cm.calculate_unitcell_volume(a, b, c, gamma=float(gamma_in))
                vol = vol * (1e-10) ** 3  # to get m^3 from A^3
                print("Please enter the number of formula units per unit cell:")
                num_fu = int(input("f.u./unit cell: "))
                if startunit == "muB/fu":
                    Tesla = cm.muB_per_fu_to_Tesla(val, num_fu, vol)
                    msg5 = (
                        f"\n{val} muB per f.u. = {Tesla:.5f} T"
                        f" ({num_fu:d} f.u./unit cell, "
                        f"cell volume = {vol:.3e} m^3)"
                    )
                    print(msg5)

                elif startunit == "T":
                    muB_fu = cm.Tesla_to_muB_per_fu(val, num_fu, vol)
                    msg6 = (
                        f"\n{val} T = {muB_fu:.5f} muB per f.u."
                        f" ({num_fu:d} f.u./unit cell, "
                        f"cell volume = {vol:.3e} m^3)"
                    )
                    print(msg6)

            else:
                cm.convert_unit(val, startunit, endunit, verbose=True)

        else:
            if r.count(" ") != 2:
                msg7 = (
                    "**Conversion syntax not recognised**\n"
                    "Please enter: value startunit endunit "
                    "(space separated) e.g. 6 T A/m\n"
                    "[q or Enter] to quit.\n"
                )
                print(msg7)
