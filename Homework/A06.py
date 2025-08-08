# Name : Siarhei Hancharou
# Assignment #: 6
# Submission Date : 12/17/2020
#
# Description:
# Visualization & UI for Data Analysis (Tkinter).
# Reuses data structures and helpers from A05:
#  - President, House classes
#  - create_president_dict(), create_house_dict()
#  - state_breakdown(house_dict)
#
# The GUI lets the user select:
#  1) President popular vote share (D/R/Other) for (year, state)
#  2) House winners party breakdown (D/R/Other) for (year, state)
# And renders a pie chart on a Tkinter Canvas.

import os
import tkinter as tk
from tkinter import messagebox


# ----------------------------- Data Classes -----------------------------

class President:
    """Represents a president record (single candidate row)."""

    def __init__(self, year, state, state_po, state_fips, state_cen,
                 state_ic, office, candidate, party, writein, candidatevotes,
                 totalvotes, version, notes):
        self.__year = year
        self.__state = state
        self.__state_po = state_po
        self.__state_fips = state_fips
        self.__state_cen = state_cen
        self.__state_ic = state_ic
        self.__office = office
        self.__candidate = candidate
        self.__party = party
        self.__writein = writein
        self.__candidatevotes = candidatevotes
        self.__totalvotes = totalvotes
        self.__version = version
        self.__notes = notes

    # accessors
    def get_year(self): return self.__year
    def get_state(self): return self.__state
    def get_state_po(self): return self.__state_po
    def get_state_fips(self): return self.__state_fips
    def get_state_cen(self): return self.__state_cen
    def get_state_ic(self): return self.__state_ic
    def get_office(self): return self.__office
    def get_candidate(self): return self.__candidate
    def get_party(self): return self.__party
    def get_writein(self): return self.__writein
    def get_candidatevotes(self): return self.__candidatevotes
    def get_totalvotes(self): return self.__totalvotes
    def get_version(self): return self.__version
    def get_notes(self): return self.__notes


class House:
    """Represents a House record (single candidate row for one district)."""

    def __init__(self, year, state, state_po, state_fips, state_cen,
                 state_ic, office, district, stage, runoff, special,
                 candidate, party, writein, mode, candidatevotes,
                 totalvotes, unofficial, version):
        self.__year = year
        self.__state = state
        self.__state_po = state_po
        self.__state_fips = state_fips
        self.__state_cen = state_cen
        self.__state_ic = state_ic
        self.__office = office
        self.__district = district
        self.__stage = stage
        self.__runoff = runoff
        self.__special = special
        self.__candidate = candidate
        self.__party = party
        self.__writein = writein
        self.__mode = mode
        self.__candidatevotes = candidatevotes
        self.__totalvotes = totalvotes
        self.__unofficial = unofficial
        self.__version = version

    # accessors
    def get_year(self): return self.__year
    def get_state(self): return self.__state
    def get_state_po(self): return self.__state_po
    def get_state_fips(self): return self.__state_fips
    def get_state_cen(self): return self.__state_cen
    def get_state_ic(self): return self.__state_ic
    def get_office(self): return self.__office
    def get_district(self): return self.__district
    def get_stage(self): return self.__stage
    def get_runoff(self): return self.__runoff
    def get_special(self): return self.__special
    def get_candidate(self): return self.__candidate
    def get_party(self): return self.__party
    def get_writein(self): return self.__writein
    def get_mode(self): return self.__mode
    def get_candidatevotes(self): return self.__candidatevotes
    def get_totalvotes(self): return self.__totalvotes
    def get_unofficial(self): return self.__unofficial
    def get_version(self): return self.__version


# ----------------------------- File Helpers -----------------------------

def _read_tab_file_lines(basename):
    """
    Read a .tab file from the same directory as this script.
    Returns list[str] (lines).
    """
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, basename)
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.readlines()


def _split_tab_and_rstrip(lines, drop_last_field=False):
    """
    Split each line by tab and rstrip each field.
    If drop_last_field is True, pop the last element (some files end with a trailing tab).
    Returns list[list[str]].
    """
    out = []
    for line in lines:
        parts = line.split("\t")
        if drop_last_field and parts:
            parts.pop(-1)
        out.append([p.rstrip() for p in parts])
    return out


# ----------------------------- Dictionaries (from A05) -----------------------------

def create_president_dict():
    """
    Build a dictionary:
      key: (year, state)  -> both strings as in the file
      value: list[President] for that (year, state)
    Keeps all rows (candidates). Later we aggregate in the GUI.
    """
    raw = _read_tab_file_lines("president.tab")
    rows = _split_tab_and_rstrip(raw, drop_last_field=True)

    # Optionally shorten overly long party strings; also map empty strings.
    cleaned = []
    for row in rows:
        tmp = []
        for idx, cell in enumerate(row):
            if idx == 8 and len(row[8]) > 20:  # party field
                tmp.append(cell[:20])
            elif cell == "":
                tmp.append("No data")
            else:
                tmp.append(cell)
        cleaned.append(tmp)

    # Group consecutive rows by (year, state)
    grouped = []
    for i in range(len(cleaned)):
        if i == 0:
            grouped.append([cleaned[i]])
            continue
        if cleaned[i][:2] == cleaned[i - 1][:2]:
            grouped[-1].append(cleaned[i])
        else:
            grouped.append([cleaned[i]])

    # Build dict
    president_dict = {}
    for bucket in grouped:
        key = (bucket[0][0], bucket[0][1])  # (year, state) as strings
        value = []
        for r in bucket:
            value.append(President(
                r[0], r[1], r[2], r[3], r[4], r[5],
                r[6], r[7], r[8], r[9], r[10], r[11], r[12], r[13]
            ))
        if key in president_dict:
            president_dict[key].extend(value)
        else:
            president_dict[key] = value

    return president_dict


def create_house_dict():
    """
    Build a dictionary:
      key: (year, state)  -> both strings as in the file
      value: list[House] rows for that (year, state)
    """
    raw = _read_tab_file_lines("house.tab")
    rows = _split_tab_and_rstrip(raw, drop_last_field=False)

    # Group consecutive rows by (year, state)
    grouped = []
    for i in range(len(rows)):
        if i == 0:
            grouped.append([rows[i]])
            continue
        if rows[i][:2] == rows[i - 1][:2]:
            grouped[-1].append(rows[i])
        else:
            grouped.append([rows[i]])

    # Build dict
    house_dict = {}
    for bucket in grouped:
        key = (bucket[0][0], bucket[0][1])  # (year, state) as strings
        value = []
        for r in bucket:
            value.append(House(
                r[0], r[1], r[2], r[3], r[4], r[5],
                r[6], r[7], r[8], r[9], r[10], r[11],
                r[12], r[13], r[14], r[15], r[16], r[17], r[18]
            ))
        if key in house_dict:
            house_dict[key].extend(value)
        else:
            house_dict[key] = value

    return house_dict


def state_breakdown(house_dict):
    """
    From a house_dict[(year, state)] -> list[House], compute per (year, state)
    the count of winners by party: {'Democrat': d, 'Republican': r, 'Other': o}.
    The "winner" for a district = candidate with max candidatevotes.
    Returns:
      dict[(int(year), state)] -> {'Democrat': d, 'Republican': r, 'Other': o}
    """
    # Build keys list skipping any potential header-like keys
    keys = [k for k in house_dict.keys() if k != ("year", "state")]

    # Build a dict of winners per (year, state) per district
    winners_by_year_state = {}
    for y, s in keys:
        # Figure out how many districts exist by scanning 'district'
        district_ids = set()
        for rec in house_dict[(y, s)]:
            # Some files store district as string; keep as int where possible
            try:
                district_ids.add(int(rec.get_district()))
            except ValueError:
                continue

        # For each district, pick max candidatevotes
        winners_for_state = {}
        for d in district_ids:
            max_votes = -1
            winner_party = None
            winner_candidate = None
            for rec in house_dict[(y, s)]:
                try:
                    if int(rec.get_district()) != d:
                        continue
                except ValueError:
                    continue
                try:
                    votes = int(rec.get_candidatevotes())
                except ValueError:
                    votes = 0
                if votes > max_votes:
                    max_votes = votes
                    winner_party = rec.get_party()
                    winner_candidate = rec.get_candidate()
            winners_for_state[d] = (winner_candidate, winner_party)

        winners_by_year_state[(y, s)] = winners_for_state

    # Count parties per (year, state)
    result = {}
    for (y, s), district_map in winners_by_year_state.items():
        d = r = o = 0
        for _, (_, party) in district_map.items():
            p = (party or "").lower()
            if p in ("democrat", "national democrat", "regular democracy",
                     "democratic-npl", "foglietta (democrat)"):
                d += 1
            elif p in ("republican", "re", "independent-republican"):
                r += 1
            else:
                o += 1
        # Coerce year to int per assignment convention
        try:
            year_int = int(y)
        except ValueError:
            # Fallback: if header or bad year, skip
            continue
        result[(year_int, s)] = {"Democrat": d, "Republican": r, "Other": o}

    return result


# ----------------------------- Tkinter GUI -----------------------------

class MyGUI:
    """
    Tkinter UI: choose a chart type, enter Year/State, render a pie chart on Canvas.
    Uses processed data from:
      - president_dictionary (raw president records)
      - state_breakdown_dict (party majority per (year, state) from House results)
    """

    def __init__(self, president_dict, state_breakdown_dict):
        # Keep references to data dictionaries
        self.__president_dict = president_dict
        self.__state_breakdown_dict = state_breakdown_dict

        # ---- Color palette (matches your screenshot theme) ----
        self.COLORS = {
            "bg": "linen",          # root background
            "panel": "linen",     
            "header_bg": "rosy brown",
            "header_fg": "white",
            "text_fg": "black",      
            "entry_bg": "white",  
            "entry_fg": "black",
            "entry_border": "#f0e2e2",
            "canvas_bg": "linen",
            "btn_bg": "white",
            "btn_ok_fg": "green4",
            "btn_quit_fg": "red",
            "btn_active_fg": "black",
            "border": "#3a3a3a",
        }

        # ---- Root window ----
        self.main_window = tk.Tk()
        self.main_window.configure(bg=self.COLORS["bg"])
        self.main_window.geometry("370x590")
        self.main_window.title("Visualization and UI for Data Analysis")

        # ---- Canvas geometry ----
        self.__CANVAS_WIDTH = 350
        self.__CANVAS_HEIGHT = 300
        self.__X1, self.__Y1, self.__X2, self.__Y2 = 30, 10, 320, 290

        # ---- Header ----
        self.top_frame = tk.Frame(self.main_window, bg=self.COLORS["panel"])
        tk.Label(
            self.top_frame,
            text="Choose which chart to draw",
            justify=tk.LEFT,
            padx=20,
            font="Times 17",
            bg=self.COLORS["header_bg"],
            fg=self.COLORS["header_fg"],
            relief=tk.GROOVE,
            width=45,
        ).pack()
        self.top_frame.pack(fill=None, expand=False)

        # ---- Radio buttons (chart selector) ----
        self.r_b_frame = tk.Frame(self.main_window, bg=self.COLORS["panel"])
        self.radio_var = tk.IntVar(value=1)
        radio_items = [
            ("Percent of Popular vote.", 1),
            ("Party affiliation House of Representatives.", 2),
        ]
        for label, val in radio_items:
            tk.Radiobutton(
                self.r_b_frame,
                text=label,
                variable=self.radio_var,
                value=val,
                padx=20,
                font="Times 17",
                bg=self.COLORS["panel"],
                fg=self.COLORS["text_fg"],
                activebackground=self.COLORS["panel"],
                activeforeground=self.COLORS["text_fg"],
                selectcolor=self.COLORS["panel"],  # keep background flat
                cursor="circle",
            ).pack(anchor=tk.W)
        self.r_b_frame.pack()

        # ---- Separator line (visual) ----
        self.year_frame_up = tk.Frame(
            self.main_window,
            width=430,
            height=6,
            relief="raised",
            borderwidth=3,
            bg=self.COLORS["panel"],
        )
        self.year_frame_up.pack()

        # ---- Year + State rows ----
        self.year_frame = tk.Frame(self.main_window, bg=self.COLORS["panel"])
        self.state_frame = tk.Frame(self.main_window, bg=self.COLORS["panel"])

        self.year_entry = tk.Entry(
            self.year_frame,
            width=10,
            bg=self.COLORS["entry_bg"],
            fg=self.COLORS["entry_fg"],
            insertbackground=self.COLORS["entry_fg"],
            highlightthickness=2,
            highlightbackground=self.COLORS["entry_border"],
            relief="flat",
        )
        self.year_label = tk.Label(
            self.year_frame,
            text="Enter Year 1976 -2016.",
            font="Times 19",
            bg=self.COLORS["panel"],
            fg=self.COLORS["text_fg"],
        )
        self.year_entry.pack(side="left")
        self.year_label.pack(side="left")

        self.state_entry = tk.Entry(
            self.state_frame,
            width=10,
            bg=self.COLORS["entry_bg"],
            fg=self.COLORS["entry_fg"],
            insertbackground=self.COLORS["entry_fg"],
            highlightthickness=2,
            highlightbackground=self.COLORS["entry_border"],
            relief="flat",
        )
        self.state_label = tk.Label(
            self.state_frame,
            text="Enter State.",
            font="Times 19",
            bg=self.COLORS["panel"],
            fg=self.COLORS["text_fg"],
        )
        self.state_entry.pack(side="left")
        self.state_label.pack(side="left")

        self.year_frame.pack()
        self.state_frame.pack()

        # ---- Second separator ----
        self.state_frame_down = tk.Frame(
            self.main_window,
            width=430,
            height=6,
            relief="raised",
            borderwidth=3,
            bg=self.COLORS["panel"],
        )
        self.state_frame_down.pack()

        # ---- Canvas ----
        self.canvas_frame = tk.Frame(self.main_window, bg=self.COLORS["panel"])
        self.canvas = tk.Canvas(
            self.canvas_frame,
            width=self.__CANVAS_WIDTH,
            height=self.__CANVAS_HEIGHT,
            bg=self.COLORS["canvas_bg"],
            highlightthickness=3,
            highlightbackground=self.COLORS["border"],
        )
        self.canvas.pack()
        self.canvas_frame.pack()

        # ---- Info rows under the canvas (legend/notes) ----
        self.middle_frame_d = tk.Frame(self.main_window, bg=self.COLORS["panel"])
        self.middle_frame_r = tk.Frame(self.main_window, bg=self.COLORS["panel"])
        self.middle_frame_o = tk.Frame(self.main_window, bg=self.COLORS["panel"])
        self.middle_frame_t = tk.Frame(self.main_window, bg=self.COLORS["panel"])
        self.middle_frame_d.pack()
        self.middle_frame_r.pack()
        self.middle_frame_o.pack()
        self.middle_frame_t.pack()

        # ---- Bottom buttons ----
        self.bottom_frame = tk.Frame(
            self.main_window, relief="raised", borderwidth=2, bg=self.COLORS["panel"]
        )
        self.new_search_button = tk.Button(
            self.bottom_frame,
            text="    Clear    ",
            fg=self.COLORS["btn_ok_fg"],
            bg=self.COLORS["btn_bg"],
            font="Times 19",
            activeforeground=self.COLORS["btn_active_fg"],
            command=self.new_search,
        )
        self.show_button = tk.Button(
            self.bottom_frame,
            text=" Show graph ",
            fg=self.COLORS["btn_ok_fg"],
            bg=self.COLORS["btn_bg"],
            font="Times 19",
            activeforeground=self.COLORS["btn_active_fg"],
            command=self.year_state,
        )
        self.show_button.bind("<Button>", self.change)
        self.quit_button = tk.Button(
            self.bottom_frame,
            text=" Quit ",
            fg=self.COLORS["btn_quit_fg"],
            bg=self.COLORS["btn_bg"],
            font="Times 19",
            activeforeground=self.COLORS["btn_active_fg"],
            command=self.main_window.destroy,
        )
        self.new_search_button.pack(side="left")
        self.show_button.pack(side="left")
        self.quit_button.pack(side="left")
        self.bottom_frame.pack(side="bottom")

        # ---- Center window on screen ----
        self.main_window.update_idletasks()
        sw, sh = self.main_window.winfo_screenwidth(), self.main_window.winfo_screenheight()
        ww, hh = map(int, self.main_window.geometry().split("+")[0].split("x"))
        self.main_window.geometry(f"+{(sw-ww)//2}+{(sh-hh)//2}")

        tk.mainloop()

    def _clear_canvas_and_notes(self):
        """Clear canvas drawings and legend/notes frames before drawing new chart."""
        self.canvas.delete("all")
        for frame in (self.middle_frame_d, self.middle_frame_r, self.middle_frame_o, self.middle_frame_t):
            for w in frame.winfo_children():
                w.destroy()

    def _note_label(self, parent, text, fg_color):
        """Create a legend label that respects theme colors."""
        lbl = tk.Label(
            parent,
            text=text,
            font="Times 15",
            bg=self.COLORS["panel"],
            fg=fg_color if fg_color else "black",
        )
        return lbl

    # Render chart based on selected radio option:
    # 1) President popular vote share (pie of D/R/Other) for (year, state)
    # 2) House winners party breakdown (pie of D/R/Other) for (year, state)
    def year_state(self):
        self._clear_canvas_and_notes()
        rb = self.radio_var.get()

        if rb == 1:
            # Popular vote shares from president_dictionary[(year, state)]
            year = self.year_entry.get()
            state = self.state_entry.get()

            # Build mapping: {totalvotes: {"democrat": x, "republican": y, "other": z}}
            dict_y_s = {}
            dict_y_s_nest = {}
            total_votes = 0
            top_two_count = 0
            other_sum = 0

            if (year, state) in self.__president_dict:
                for rec in self.__president_dict[(year, state)]:
                    if top_two_count < 2:
                        dict_y_s_nest[rec.get_party()] = rec.get_candidatevotes()
                        total_votes = rec.get_totalvotes()
                        top_two_count += 1
                    else:
                        try:
                            other_sum += int(rec.get_candidatevotes())
                        except ValueError:
                            pass
                dict_y_s_nest["other"] = other_sum
                dict_y_s[total_votes] = dict_y_s_nest

            # Extract numeric values
            d_votes = r_votes = o_votes = 0
            total = 0
            for total in dict_y_s:
                for party in dict_y_s[total]:
                    if party == "democrat":
                        d_votes = dict_y_s[total][party]
                    elif party == "republican":
                        r_votes = dict_y_s[total][party]
                    elif party == "other":
                        o_votes = dict_y_s[total][party]

            # Choose primary slice order/colors
            one = two = 0.0
            fill_1 = fill_2 = ""
            if d_votes > r_votes:
                one = float(d_votes) / float(total) * 360 if total else 0
                two = float(r_votes) / float(total) * 360 if total else 0
                fill_1, fill_2 = "blue", "red"
            elif r_votes > d_votes:
                one = float(r_votes) / float(total) * 360 if total else 0
                two = float(d_votes) / float(total) * 360 if total else 0
                fill_1, fill_2 = "red", "blue"

            try:
                incr_two = one + two
                three = float(o_votes) / float(total) * 360 if total else 0

                # Draw pie arcs
                self.canvas.create_arc(self.__X1, self.__Y1, self.__X2, self.__Y2,
                                       start=0, extent=one, fill=fill_1)
                self.canvas.create_arc(self.__X1, self.__Y1, self.__X2, self.__Y2,
                                       start=one, extent=two, fill=fill_2)
                self.canvas.create_arc(self.__X1, self.__Y1, self.__X2, self.__Y2,
                                       start=incr_two, extent=three, fill="green")

                # Legend
                d = round(float(d_votes) / float(total) * 100, 2) if total else 0.0
                r = round(float(r_votes) / float(total) * 100, 2) if total else 0.0
                o = round(float(o_votes) / float(total) * 100, 2) if total else 0.0

                self._note_label(self.middle_frame_d, f"  Democrat = {d}%", "blue").pack(side="left")
                self._note_label(self.middle_frame_r, f"Republican = {r}%", "red").pack(side="left")
                self._note_label(self.middle_frame_o, f"      Other = {o}%", "green").pack(side="left")

            except ZeroDivisionError:
                messagebox.showerror(title="Error", message="Check the entered data (Year/State).")

        elif rb == 2:
            # House winners by party from state_breakdown_dict[(int(year), state)]
            year = self.year_entry.get()
            state = self.state_entry.get()

            d_votes = r_votes = o_votes = 0
            total = 0

            if year.isdigit() and (int(year), state) in self.__state_breakdown_dict:
                by_party = self.__state_breakdown_dict[(int(year), state)]
                d_votes = by_party.get("Democrat", 0)
                r_votes = by_party.get("Republican", 0)
                o_votes = by_party.get("Other", 0)
                total = d_votes + r_votes + o_votes

            # Choose primary slice order/colors
            one = two = 0.0
            fill_1 = fill_2 = ""
            if d_votes > r_votes:
                one = int(d_votes) / int(total) * 360 if total else 0
                two = int(r_votes) / int(total) * 360 if total else 0
                fill_1, fill_2 = "blue", "red"
            elif r_votes > d_votes:
                one = int(r_votes) / int(total) * 360 if total else 0
                two = int(d_votes) / int(total) * 360 if total else 0
                fill_1, fill_2 = "red", "blue"

            try:
                incr_two = one + two
                three = int(o_votes) / int(total) * 360 if total else 0

                # Draw pie arcs
                self.canvas.create_arc(self.__X1, self.__Y1, self.__X2, self.__Y2,
                                       start=0, extent=one, fill=fill_1)
                self.canvas.create_arc(self.__X1, self.__Y1, self.__X2, self.__Y2,
                                       start=one, extent=two, fill=fill_2)
                self.canvas.create_arc(self.__X1, self.__Y1, self.__X2, self.__Y2,
                                       start=incr_two, extent=three, fill="green")

                # Legend
                self._note_label(self.middle_frame_d, f"   Democrat = {d_votes} votes.", "blue").pack(side="left")
                self._note_label(self.middle_frame_r, f"Republican = {r_votes} votes.", "red").pack(side="left")
                self._note_label(self.middle_frame_o, f"       Other = {o_votes} votes.", "green").pack(side="left")
                self._note_label(self.middle_frame_t, f"Total votes = {total} votes.", None).pack(side="left")

            except ZeroDivisionError:
                messagebox.showerror(title="Error", message="Check the entered data (Year/State).")

    # Visual feedback: change button color on click
    def change(self, _event):
        self.show_button["fg"] = self.COLORS["btn_active_fg"]
        self.show_button["activeforeground"] = self.COLORS["btn_active_fg"]

    # Reset UI by closing current window and opening a fresh one
    def new_search(self):
        self.main_window.destroy()
        MyGUI(president_dictionary, state_breakdown_dict)


# ----------------------------- Entry Point -----------------------------

if __name__ == "__main__":
    # Build dictionaries once and pass into GUI
    president_dictionary = create_president_dict()
    house_dictionary = create_house_dict()
    state_breakdown_dict = state_breakdown(house_dictionary)

    # Launch GUI
    my_gui = MyGUI(president_dictionary, state_breakdown_dict)
