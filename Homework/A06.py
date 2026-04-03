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

        # ---- Color palette (keeps your warm tones, but with cleaner contrast) ----
        self.COLORS = {
            "bg": "#f4ece5",
            "surface": "#fbf5ef",
            "panel": "#f0e3d7",
            "header_bg": "#be9790",
            "header_fg": "#fff8f4",
            "text_fg": "#2f2622",
            "muted_fg": "#6e5c55",
            "entry_bg": "#fffdfb",
            "entry_fg": "#2f2622",
            "entry_border": "#d9c0b8",
            "canvas_bg": "#fffaf5",
            "canvas_ring": "#dcc3bb",
            "btn_neutral_bg": "#fff8f2",
            "btn_show_bg": "#dcc0b0",
            "btn_clear_fg": "#2f7d32",
            "btn_show_fg": "#4b342c",
            "btn_quit_fg": "#b33636",
            "btn_border": "#b99b92",
            "btn_active_fg": "#241d1a",
            "border": "#8e7269",
            "shadow": "#d3b8af",
            "democrat": "#2048f2",
            "republican": "#f23628",
            "other": "#3e8f2e",
        }

        self.FONTS = {
            "title": ("Times New Roman", 20, "bold"),
            "subtitle": ("Times New Roman", 11),
            "section": ("Times New Roman", 15, "bold"),
            "body": ("Times New Roman", 14),
            "radio": ("Times New Roman", 15),
            "field_label": ("Times New Roman", 12, "bold"),
            "field_hint": ("Times New Roman", 10),
            "button": ("Times New Roman", 15, "bold"),
            "legend": ("Times New Roman", 14, "bold"),
            "canvas_title": ("Times New Roman", 14, "bold"),
            "canvas_hint": ("Times New Roman", 12),
        }

        # ---- Root window ----
        self.main_window = tk.Tk()
        self.main_window.configure(bg=self.COLORS["bg"])
        self.main_window.geometry("760x820")
        self.main_window.minsize(620, 680)
        self.main_window.title("Visualization and UI for Data Analysis")
        self.main_window.option_add("*Label.Background", self.COLORS["bg"])

        # ---- Canvas geometry ----
        self.__DEFAULT_CANVAS_WIDTH = 480
        self.__DEFAULT_CANVAS_HEIGHT = 370
        self.__MIN_CANVAS_WIDTH = 300
        self.__MIN_CANVAS_HEIGHT = 180
        self.__MAX_CANVAS_WIDTH = 640
        self.__MAX_CANVAS_HEIGHT = 460
        self.__CANVAS_WIDTH = self.__DEFAULT_CANVAS_WIDTH
        self.__CANVAS_HEIGHT = self.__DEFAULT_CANVAS_HEIGHT
        self._current_view = {"kind": "placeholder"}
        self._resize_job = None

        self.main_frame = tk.Frame(self.main_window, bg=self.COLORS["bg"], padx=28, pady=26)
        self.main_frame.pack(fill="both", expand=True)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)

        self.header_frame = tk.Frame(
            self.main_frame,
            bg=self.COLORS["header_bg"],
            bd=1,
            relief="solid",
            padx=24,
            pady=16,
        )
        self.header_frame.grid(row=0, column=0, sticky="ew")
        tk.Label(
            self.header_frame,
            text="Election Data Visualization",
            font=self.FONTS["title"],
            bg=self.COLORS["header_bg"],
            fg=self.COLORS["header_fg"],
        ).pack()
        tk.Label(
            self.header_frame,
            text="Choose the chart, enter a year and state, then render a clean election summary.",
            font=self.FONTS["subtitle"],
            bg=self.COLORS["header_bg"],
            fg=self.COLORS["header_fg"],
        ).pack(pady=(6, 0))

        self.controls_card = tk.Frame(
            self.main_frame,
            bg=self.COLORS["surface"],
            bd=1,
            relief="solid",
            padx=24,
            pady=20,
        )
        self.controls_card.grid(row=1, column=0, sticky="ew", pady=(18, 16))

        self._section_label(self.controls_card, "Chart Type").pack(anchor="w")

        self.radio_var = tk.IntVar(value=1)
        radio_items = [
            ("Percent of popular vote", 1),
            ("Party affiliation in the House of Representatives", 2),
        ]
        self.r_b_frame = tk.Frame(self.controls_card, bg=self.COLORS["surface"])
        self.r_b_frame.pack(fill="x", pady=(8, 16))
        for label, val in radio_items:
            tk.Radiobutton(
                self.r_b_frame,
                text=label,
                variable=self.radio_var,
                value=val,
                font=self.FONTS["radio"],
                bg=self.COLORS["surface"],
                fg=self.COLORS["text_fg"],
                selectcolor=self.COLORS["surface"],
                activebackground=self.COLORS["surface"],
                activeforeground=self.COLORS["text_fg"],
                anchor="w",
                padx=4,
                cursor="hand2",
            ).pack(fill="x", pady=3)

        self.separator = tk.Frame(self.controls_card, bg=self.COLORS["entry_border"], height=1)
        self.separator.pack(fill="x", pady=(0, 18))

        self.form_frame = tk.Frame(self.controls_card, bg=self.COLORS["surface"])
        self.form_frame.pack(fill="x")

        self.year_field = tk.Frame(self.form_frame, bg=self.COLORS["surface"])
        self.year_field.pack(side="left", fill="x", expand=True, padx=(0, 12))
        tk.Label(
            self.year_field,
            text="Year",
            font=self.FONTS["field_label"],
            bg=self.COLORS["surface"],
            fg=self.COLORS["text_fg"],
        ).pack(anchor="w")
        tk.Label(
            self.year_field,
            text="Valid range: 1976-2016",
            font=self.FONTS["field_hint"],
            bg=self.COLORS["surface"],
            fg=self.COLORS["muted_fg"],
        ).pack(anchor="w", pady=(2, 6))
        self.year_entry = tk.Entry(
            self.year_field,
            width=18,
            font=self.FONTS["body"],
            bg=self.COLORS["entry_bg"],
            fg=self.COLORS["entry_fg"],
            insertbackground=self.COLORS["entry_fg"],
            relief="flat",
            highlightthickness=2,
            highlightbackground=self.COLORS["entry_border"],
            highlightcolor=self.COLORS["border"],
            bd=0,
        )
        self.year_entry.pack(fill="x", ipady=8)

        self.state_field = tk.Frame(self.form_frame, bg=self.COLORS["surface"])
        self.state_field.pack(side="left", fill="x", expand=True, padx=(12, 0))
        tk.Label(
            self.state_field,
            text="State",
            font=self.FONTS["field_label"],
            bg=self.COLORS["surface"],
            fg=self.COLORS["text_fg"],
        ).pack(anchor="w")
        tk.Label(
            self.state_field,
            text="Example: California",
            font=self.FONTS["field_hint"],
            bg=self.COLORS["surface"],
            fg=self.COLORS["muted_fg"],
        ).pack(anchor="w", pady=(2, 6))
        self.state_entry = tk.Entry(
            self.state_field,
            width=18,
            font=self.FONTS["body"],
            bg=self.COLORS["entry_bg"],
            fg=self.COLORS["entry_fg"],
            insertbackground=self.COLORS["entry_fg"],
            relief="flat",
            highlightthickness=2,
            highlightbackground=self.COLORS["entry_border"],
            highlightcolor=self.COLORS["border"],
            bd=0,
        )
        self.state_entry.pack(fill="x", ipady=8)

        self.chart_card = tk.Frame(
            self.main_frame,
            bg=self.COLORS["surface"],
            bd=1,
            relief="solid",
            padx=22,
            pady=20,
        )
        self.chart_card.grid(row=2, column=0, sticky="nsew")

        chart_heading = tk.Frame(self.chart_card, bg=self.COLORS["surface"])
        chart_heading.pack(fill="x")
        tk.Label(
            chart_heading,
            text="Visualization",
            font=self.FONTS["section"],
            bg=self.COLORS["surface"],
            fg=self.COLORS["text_fg"],
        ).pack(anchor="w")
        tk.Label(
            chart_heading,
            text="The chart is centered and the legend stays visually attached to the graph.",
            font=self.FONTS["field_hint"],
            bg=self.COLORS["surface"],
            fg=self.COLORS["muted_fg"],
        ).pack(anchor="w", pady=(2, 12))

        self.canvas_frame = tk.Frame(
            self.chart_card,
            bg=self.COLORS["canvas_bg"],
            bd=1,
            relief="solid",
            padx=14,
            pady=14,
        )
        self.canvas_frame.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(
            self.canvas_frame,
            width=self.__CANVAS_WIDTH,
            height=self.__CANVAS_HEIGHT,
            bg=self.COLORS["canvas_bg"],
            highlightthickness=0,
            bd=0,
        )
        self.canvas.pack(fill="both", expand=True)

        self.summary_frame = tk.Frame(self.chart_card, bg=self.COLORS["surface"])
        self.summary_frame.pack(fill="x", pady=(14, 0))

        self.bottom_frame = tk.Frame(self.main_frame, bg=self.COLORS["bg"])
        self.bottom_frame.grid(row=3, column=0, sticky="ew", pady=(18, 0))

        self.new_search_button = self._action_button(
            self.bottom_frame,
            text="Clear",
            fg=self.COLORS["btn_clear_fg"],
            bg=self.COLORS["btn_neutral_bg"],
            command=self.new_search,
        )
        self.show_button = self._action_button(
            self.bottom_frame,
            text="Show Graph",
            fg=self.COLORS["btn_show_fg"],
            bg=self.COLORS["btn_show_bg"],
            command=self.year_state,
        )
        self.quit_button = self._action_button(
            self.bottom_frame,
            text="Quit",
            fg=self.COLORS["btn_quit_fg"],
            bg=self.COLORS["btn_neutral_bg"],
            command=self.main_window.destroy,
        )
        self.new_search_button.pack(side="left", expand=True, fill="x", padx=(0, 8))
        self.show_button.pack(side="left", expand=True, fill="x", padx=8)
        self.quit_button.pack(side="left", expand=True, fill="x", padx=(8, 0))

        self._draw_placeholder()
        self.year_entry.focus_set()
        self.main_window.bind("<Configure>", self._on_window_resize)

        # ---- Center window on screen ----
        self.main_window.update_idletasks()
        sw, sh = self.main_window.winfo_screenwidth(), self.main_window.winfo_screenheight()
        ww, hh = map(int, self.main_window.geometry().split("+")[0].split("x"))
        self.main_window.geometry(f"+{(sw-ww)//2}+{(sh-hh)//2}")

        tk.mainloop()

    def _clear_canvas_and_notes(self):
        """Clear canvas drawings and legend/notes frames before drawing new chart."""
        self.canvas.delete("all")
        for widget in self.summary_frame.winfo_children():
            widget.destroy()
        self.legend_row = None

    def _on_window_resize(self, event):
        if event.widget != self.main_window:
            return
        if self._resize_job is not None:
            self.main_window.after_cancel(self._resize_job)
        self._resize_job = self.main_window.after(80, self._apply_responsive_layout)

    def _apply_responsive_layout(self):
        self._resize_job = None
        self.main_window.update_idletasks()

        available_width = self.canvas_frame.winfo_width() - 28
        available_height = self.canvas_frame.winfo_height() - 28
        canvas_width = min(self.__MAX_CANVAS_WIDTH, max(self.__MIN_CANVAS_WIDTH, available_width))
        canvas_height = min(self.__MAX_CANVAS_HEIGHT, max(self.__MIN_CANVAS_HEIGHT, available_height))

        if (
            canvas_width == self.__CANVAS_WIDTH
            and canvas_height == self.__CANVAS_HEIGHT
        ):
            return

        self.__CANVAS_WIDTH = canvas_width
        self.__CANVAS_HEIGHT = canvas_height
        self.canvas.config(width=self.__CANVAS_WIDTH, height=self.__CANVAS_HEIGHT)
        self._render_current_view()

    def _section_label(self, parent, text):
        return tk.Label(
            parent,
            text=text,
            font=self.FONTS["section"],
            bg=parent.cget("bg"),
            fg=self.COLORS["text_fg"],
        )

    def _action_button(self, parent, text, fg, bg, command):
        return tk.Button(
            parent,
            text=text,
            command=command,
            font=self.FONTS["button"],
            fg=fg,
            bg=bg,
            activeforeground=self.COLORS["btn_active_fg"],
            activebackground=self.COLORS["surface"],
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=10,
            pady=12,
            highlightthickness=1,
            highlightbackground=self.COLORS["btn_border"],
        )

    def _normalize_state(self, state):
        normalized = state.strip().lower()
        if normalized in ("dc", "d.c.", "district of columbia"):
            return "District of Columbia"

        minor_words = {"of", "and", "the"}
        words = normalized.split()
        output = []
        for index, word in enumerate(words):
            if index > 0 and word in minor_words:
                output.append(word)
            else:
                output.append(word.capitalize())
        return " ".join(output)

    def _chart_bounds(self):
        canvas_width = max(self.__MIN_CANVAS_WIDTH, self.canvas.winfo_width())
        canvas_height = max(self.__MIN_CANVAS_HEIGHT, self.canvas.winfo_height())

        top_margin = 56
        bottom_margin = 18
        side_margin = 28
        usable_width = max(120, canvas_width - (2 * side_margin))
        usable_height = max(120, canvas_height - top_margin - bottom_margin)
        diameter = min(usable_width, usable_height)
        x1 = (canvas_width - diameter) / 2
        y1 = top_margin + max(0, (usable_height - diameter) / 2)
        x2 = x1 + diameter
        y2 = y1 + diameter
        return canvas_width, canvas_height, x1, y1, x2, y2

    def _render_current_view(self):
        kind = self._current_view.get("kind")
        if kind == "chart":
            self._draw_pie_chart(
                title=self._current_view["title"],
                counts=self._current_view["counts"],
                total=self._current_view["total"],
                formatter_kind=self._current_view["formatter_kind"],
                remember=False,
            )
            if self._current_view["formatter_kind"] == "seats":
                self._legend_line(f"Total seats = {self._current_view['total']}", None)
        else:
            self._draw_placeholder(remember=False)

    def _draw_placeholder(self, remember=True):
        if remember:
            self._current_view = {"kind": "placeholder"}

        self._clear_canvas_and_notes()
        canvas_width, canvas_height, x1, y1, x2, y2 = self._chart_bounds()
        self.canvas.create_rectangle(
            12,
            12,
            canvas_width - 12,
            canvas_height - 12,
            outline=self.COLORS["canvas_ring"],
            width=2,
        )
        self.canvas.create_oval(
            x1,
            y1,
            x2,
            y2,
            outline=self.COLORS["canvas_ring"],
            width=2,
        )
        self.canvas.create_text(
            canvas_width / 2,
            34,
            text="Your chart will appear here",
            fill=self.COLORS["text_fg"],
            font=self.FONTS["canvas_title"],
        )
        self.canvas.create_text(
            canvas_width / 2,
            canvas_height / 2,
            text="Enter a valid year and state,\nthen click Show Graph.",
            fill=self.COLORS["muted_fg"],
            font=self.FONTS["canvas_hint"],
            justify="center",
        )

        tk.Label(
            self.summary_frame,
            text="No chart is displayed yet.",
            font=self.FONTS["legend"],
            bg=self.COLORS["surface"],
            fg=self.COLORS["muted_fg"],
        ).pack(anchor="center")

    def _note_label(self, parent, text, fg_color):
        """Create a legend label that respects theme colors."""
        return tk.Label(
            parent,
            text=text,
            font=self.FONTS["legend"],
            bg=self.COLORS["surface"],
            fg=fg_color if fg_color else self.COLORS["text_fg"],
            anchor="center",
        )

    def _legend_line(self, text, color):
        if self.legend_row is None:
            self.legend_row = tk.Frame(self.summary_frame, bg=self.COLORS["surface"])
            self.legend_row.pack(anchor="center", pady=2)

        line = tk.Frame(self.legend_row, bg=self.COLORS["surface"])
        line.pack(side="left", padx=18)
        marker = tk.Frame(
            line,
            width=12,
            height=12,
            bg=color if color else self.COLORS["muted_fg"],
            bd=0,
        )
        marker.pack(side="left", padx=(0, 8))
        marker.pack_propagate(False)
        self._note_label(line, text, color).pack(side="left")

    def _read_form_inputs(self):
        year = self.year_entry.get().strip()
        state = self._normalize_state(self.state_entry.get())

        if not year or not state:
            raise ValueError("Enter both a year and a state.")
        if not year.isdigit():
            raise ValueError("Year must contain only digits.")
        if not 1976 <= int(year) <= 2016:
            raise ValueError("Year must be between 1976 and 2016.")

        return year, state

    def _president_chart_data(self, year, state):
        key = (year, state)
        if key not in self.__president_dict:
            raise ValueError(f"No popular-vote data found for {state} in {year}.")

        counts = {"Democrat": 0, "Republican": 0, "Other": 0}
        total_votes = 0
        for rec in self.__president_dict[key]:
            try:
                votes = int(rec.get_candidatevotes())
            except ValueError:
                votes = 0

            try:
                total_votes = int(rec.get_totalvotes())
            except ValueError:
                pass

            party = (rec.get_party() or "").strip().lower()
            if party == "democrat":
                counts["Democrat"] += votes
            elif party == "republican":
                counts["Republican"] += votes
            else:
                counts["Other"] += votes

        if total_votes <= 0:
            total_votes = counts["Democrat"] + counts["Republican"] + counts["Other"]

        if total_votes <= 0:
            raise ValueError(f"Vote totals are missing for {state} in {year}.")

        return counts, total_votes

    def _house_chart_data(self, year, state):
        key = (int(year), state)
        if key not in self.__state_breakdown_dict:
            raise ValueError(f"No House data found for {state} in {year}.")

        by_party = self.__state_breakdown_dict[key]
        counts = {
            "Democrat": by_party.get("Democrat", 0),
            "Republican": by_party.get("Republican", 0),
            "Other": by_party.get("Other", 0),
        }
        total = counts["Democrat"] + counts["Republican"] + counts["Other"]
        if total <= 0:
            raise ValueError(f"House totals are missing for {state} in {year}.")
        return counts, total

    def _draw_chart_shell(self, title):
        canvas_width, canvas_height, _, _, _, _ = self._chart_bounds()
        self.canvas.create_rectangle(
            12,
            12,
            canvas_width - 12,
            canvas_height - 12,
            outline=self.COLORS["canvas_ring"],
            width=2,
        )
        self.canvas.create_text(
            canvas_width / 2,
            34,
            text=title,
            fill=self.COLORS["text_fg"],
            font=self.FONTS["canvas_title"],
        )

    def _format_legend_value(self, formatter_kind, label, value, total):
        if formatter_kind == "percent":
            return f"{label} = {round((value / total) * 100, 2)}%"
        return f"{label} = {value} seats"

    def _draw_pie_chart(self, title, counts, total, formatter_kind, remember=True):
        if remember:
            self._current_view = {
                "kind": "chart",
                "title": title,
                "counts": counts.copy(),
                "total": total,
                "formatter_kind": formatter_kind,
            }

        self._clear_canvas_and_notes()
        self._draw_chart_shell(title)
        _, _, x1, y1, x2, y2 = self._chart_bounds()

        slices = [
            ("Democrat", counts["Democrat"], self.COLORS["democrat"]),
            ("Republican", counts["Republican"], self.COLORS["republican"]),
            ("Other", counts["Other"], self.COLORS["other"]),
        ]

        start_angle = 90
        for label, value, color in slices:
            extent = (value / total) * 360 if total else 0
            if extent <= 0:
                continue
            self.canvas.create_arc(
                x1,
                y1,
                x2,
                y2,
                start=start_angle,
                extent=-extent,
                fill=color,
                outline=self.COLORS["canvas_bg"],
                width=2,
            )
            start_angle -= extent

        self.canvas.create_oval(
            x1,
            y1,
            x2,
            y2,
            outline=self.COLORS["border"],
            width=2,
        )

        for label, value, color in slices:
            self._legend_line(self._format_legend_value(formatter_kind, label, value, total), color)

    # Render chart based on selected radio option:
    # 1) President popular vote share (pie of D/R/Other) for (year, state)
    # 2) House winners party breakdown (pie of D/R/Other) for (year, state)
    def year_state(self):
        try:
            year, state = self._read_form_inputs()
            rb = self.radio_var.get()

            if rb == 1:
                counts, total = self._president_chart_data(year, state)
                self._draw_pie_chart(
                    title=f"Popular Vote in {state}, {year}",
                    counts=counts,
                    total=total,
                    formatter_kind="percent",
                )
            else:
                counts, total = self._house_chart_data(year, state)
                self._draw_pie_chart(
                    title=f"House Winners in {state}, {year}",
                    counts=counts,
                    total=total,
                    formatter_kind="seats",
                )
                self._legend_line(f"Total seats = {total}", None)

            self.change(None)

        except ValueError as error:
            self._draw_placeholder()
            messagebox.showerror(title="Error", message=str(error))

    # Visual feedback: change button color on click
    def change(self, _event):
        self.show_button["fg"] = self.COLORS["btn_active_fg"]
        self.show_button["activeforeground"] = self.COLORS["btn_active_fg"]

    # Reset UI without recreating the entire application window
    def new_search(self):
        self.year_entry.delete(0, tk.END)
        self.state_entry.delete(0, tk.END)
        self.show_button["fg"] = self.COLORS["btn_show_fg"]
        self.show_button["activeforeground"] = self.COLORS["btn_active_fg"]
        self._draw_placeholder()
        self.year_entry.focus_set()


# ----------------------------- Entry Point -----------------------------

if __name__ == "__main__":
    # Build dictionaries once and pass into GUI
    president_dictionary = create_president_dict()
    house_dictionary = create_house_dict()
    state_breakdown_dict = state_breakdown(house_dictionary)

    # Launch GUI
    my_gui = MyGUI(president_dictionary, state_breakdown_dict)
