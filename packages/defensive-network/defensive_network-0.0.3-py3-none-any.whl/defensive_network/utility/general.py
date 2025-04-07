import accessible_space.utility
import streamlit.errors
import tqdm
import streamlit as st
import wfork_streamlit_profiler as streamlit_profiler


class _Sentinel:
    def __eq__(self, other):
        return isinstance(other, _Sentinel)


_unset = _Sentinel()  # To explicitly differentiate between a default None and a user-set None


def get_number_of_lines_in_file(file_path):
    with open(file_path) as f:
        return sum(1 for _ in f)


def is_run_within_streamlit():
    """
    >>> is_run_within_streamlit()
    False
    """
    return st.runtime.exists()


progress_bar = accessible_space.utility.progress_bar


# def progress_bar(iterable, update_interval=1, **kwargs):
#     """
#     >>> for i in progress_bar(range(100), total=100, desc="Testing progress_bar"):
#     ...     pass
#     """
#     yield accessible_space.utility.progress_bar(iterable, update_interval, **kwargs)
#     update_interval = 1
#
#     try:
#         total = kwargs["total"]
#         kwargs.pop("total")
#     except KeyError:
#         try:
#             total = len(iterable)
#         except TypeError:
#             total = None
#
#     def _get_progress_text_without_progress_bar(console_progress_bar):
#         return str(console_progress_bar).replace("█", "").replace("▌", "").replace("▊", "").replace("▍", "").replace("▋", "").replace("▉", "").replace("▏", "").replace("▎", "")
#
#     console_progress_bar = tqdm.tqdm(iterable, total=total, **kwargs)#CustomTqdm(**kwargs)
#
#     if is_run_within_streamlit():
#         st.empty()
#         streamlit_progress_bar = st.progress(0)
#         try:
#             streamlit_progress_bar.progress(0, text=_get_progress_text_without_progress_bar(console_progress_bar))
#         except streamlit.errors.NoSessionContext:
#             pass
#     else:
#         streamlit_progress_bar = None
#
#     for i, item in enumerate(console_progress_bar):
#         yield item
#         if i % update_interval == 0:
#             if total is not None:
#                 progress_value = (i + 1) / total
#             else:
#                 progress_value = 0
#
#             if streamlit_progress_bar is not None:
#                 try:
#                     streamlit_progress_bar.progress(progress_value, text=_get_progress_text_without_progress_bar(console_progress_bar))
#                 except streamlit.errors.NoSessionContext:
#                     pass
#
#     if streamlit_progress_bar is not None:
#         try:
#             streamlit_progress_bar.progress(0.999, text=_get_progress_text_without_progress_bar(console_progress_bar))
#         except streamlit.errors.NoSessionContext:
#             pass



_profiler = None

def start_streamlit_profiler():
    global _profiler
    if _profiler is None:
        _profiler = streamlit_profiler.Profiler()
        try:
            _profiler.start()
        except RuntimeError:
            pass


def stop_streamlit_profiler():
    global _profiler
    if _profiler is not None:
        try:
            _profiler.stop()
        except RuntimeError:
            pass
        _profiler = None


def extract_numbers_from_string_as_ints(text):
    """
    >>> extract_numbers_from_string_as_ints("There are 3.1 apples, 4 bananas, and 12 oranges.")
    [3, 1, 4, 12]
    """
    import re
    numbers_as_strings = re.findall(r'\d+', text)
    return [int(num) for num in numbers_as_strings]


def uniquify_keep_order(lst):
    """
    >>> uniquify_keep_order([1, 2, 3, 1, 2, 4])
    [1, 2, 3, 4]
    """
    return list(dict.fromkeys(lst))


def seconds_since_period_start_to_mmss(seconds, period_nr):
    """
    >>> seconds_since_period_start_to_mmss(100, 0)
    '01:40'
    >>> seconds_since_period_start_to_mmss(45*60+123, 0)
    '45+2:03'
    >>> seconds_since_period_start_to_mmss(45*60+123, 1)
    '90+2:03'
    >>> seconds_since_period_start_to_mmss(-66, 1)
    '45-1:06'
    """
    assert period_nr in {0, 1}, f"period_nr={period_nr} not in {{0, 1}}"

    mins = int(seconds // 60)
    if mins >= 45:
        mins = 45
        extra_min_string = f"+{int((seconds - 45 * 60) // 60)}"
    elif mins < 0:
        mins = 0
        seconds = -seconds
        extra_min_string = f"-{int(seconds // 60)}"
    else:
        extra_min_string = ""

    if period_nr == 1:
        mins += 45

    return f"{mins:02d}{extra_min_string}:{int(seconds % 60):02d}"
