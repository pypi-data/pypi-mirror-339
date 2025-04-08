from pathlib import Path


def comments_write(name_path, MetaList):
    """Function to write in an independent file the comment strings"""

    Path(name_path).parent.mkdir(parents=True, exist_ok=True)
    name = name_path.parent.absolute() / (name_path.name + "_comments.txt")

    with open(file=name, mode="w", encoding="utf-8") as outfile:
        for m in MetaList:
            outfile.write(m.Comments + "\n")


def summary_write(name_path, MetaList):

    Path(name_path).parent.mkdir(parents=True, exist_ok=True)
    name = name_path.parent.absolute() / (name_path.name + "_summary.txt")

    with open(file=name, mode="w", encoding="utf-8") as outfile:
        header = f"  Cell Id{'':5s}Mat Id{'':6s}Density{'':7s}Volume{'':5s}Comments\n"
        outfile.write(header)

        for m in MetaList:
            if m.Void or m.__id__ is None:
                continue
            index = m.__id__
            Vol = m.Volume * 1e-3
            if m.Material == 0:
                line = " {:>8d}{:3s}{:>8d}{:3s}{:11s}{:3s}{:11.4e}{:3s}{}\n".format(
                    index, "", 0, "", "", "", Vol, "", m.Comments
                )
            else:
                if abs(m.Density) < 1e-2:
                    line = " {:>8d}{:3s}{:>8d}{:3s}{:11.4e}{:3s}{:11.4e}{:3s}{}\n".format(
                        index,
                        "",
                        m.Material,
                        "",
                        m.Density,
                        "",
                        Vol,
                        "",
                        m.Comments,
                    )
                else:
                    line = " {:>8d}{:3s}{:>8d}{:3s}{:11.7f}{:3s}{:11.4e}{:3s}{}\n".format(
                        index,
                        "",
                        m.Material,
                        "",
                        m.Density,
                        "",
                        Vol,
                        "",
                        m.Comments,
                    )

            outfile.write(line)
