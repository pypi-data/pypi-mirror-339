import ipywidgets as widgets
from typing import Any
from ipyquizjb.types import QuestionWidgetPackage, EvaluationFunction, FeedbackFunction
from ipyquizjb.utils import get_evaluation_color, standard_feedback, disable_input, question_title


def generic_question(question: str,
                     input_widget: widgets.Widget,
                     evaluation_function: EvaluationFunction,
                     feedback: FeedbackFunction = standard_feedback) -> QuestionWidgetPackage:
    """
    Abstract question function used by the other question types to display questions.
    A question type function calls this function with a provided input_widget and
    an evaluation_function that gives a score based on that input widget.
    The optional feedback function can be used to specify what feedback should
    be given based on the evaluation score.

    It returns a tuple consisting of:
    - A ipywidgets.Box of the interactive elements
    - evaluation_function
    - A callback function that will provide feedback 
    to the question when called 

    Parameters:
    - question: Question body
    - input_widget: Widget used for getting user input
    - evaluation_function: a function returning an evaluation of the answer provided based on the input widget
    - feedback: A function giving textual feedback based on the result of the evaluation_function
    """
    question_body_widget = question_title(question)

    output = widgets.Output()
    output.layout = {"padding": "0.25em", "margin": "0.2em"}

    def feedback_callback():
        evaluation = evaluation_function()

        with output:
            # Clear output in case of successive calls
            output.clear_output()

            # Print feedback to output
            print(feedback(evaluation))

            # Sets border color based on evaluation
            output.layout.border_left = f"solid {get_evaluation_color(evaluation)} 1em"

        if evaluation is not None and evaluation != 1:
            # Only disable on wrong input, not when not answered
            disable_input(input_widget)

    layout = widgets.VBox([
        question_body_widget,
        widgets.HBox([input_widget],
                     layout=widgets.Layout(padding="0.5em")),
        widgets.VBox([output]),
    ],
        layout=dict(border_bottom="solid", border_top="solid",
                    padding="0.2em"))

    return layout, evaluation_function, feedback_callback


def multiple_choice(question: str,
                    options: list[Any],
                    correct_option: Any) -> QuestionWidgetPackage:
    """
    Multiple-choice-single-answer type question.

    Delegates to generic_question.
    """
    options_widget = widgets.ToggleButtons(
        options=options,
        value=None,
        disabled=False,
        style={"button_width": "auto"},
    )

    def evaluation_function():
        if options_widget.value is None:
            return None
        return float(options_widget.value == correct_option)

    return generic_question(question=question,
                            input_widget=options_widget,
                            evaluation_function=evaluation_function)


def multiple_answers(question: str,
                     options: list[Any],
                     correct_answers: list[Any]) -> QuestionWidgetPackage:
    """
    Multiple-choice-multiple-answers type question.

    Delegates to generic_question.

    """
    buttons = [widgets.ToggleButton(
        value=False, description=option) for option in options]

    def feedback(evaluation_result):
        if evaluation_result == None:
            return "Please pick an answer"
        elif evaluation_result == 0:
            return "Incorrect answer"
        else:
            return f"Correct answers: {evaluation_result}/{len(correct_answers)}"

    def evaluation_function():
        # Returns the proportion of correct answers.

        answers = set(
            button.description for button in buttons if button.value)
        if len(answers) == 0:
            return None

        num_correct_answers = len(answers.intersection(correct_answers))

        return num_correct_answers / len(correct_answers)

    return generic_question(question=question,
                            input_widget=widgets.HBox(buttons),
                            evaluation_function=evaluation_function,
                            feedback=feedback)


def numeric_input(question: str, correct_answer: float) -> QuestionWidgetPackage:
    """
    Question with box for numeric input.

    Delegates to generic_question.
    """

    input_widget = widgets.FloatText(
        value=None,
    )

    def evaluation_function():
        if input_widget.value is None:
            return None
        return float(input_widget.value == correct_answer)

    return generic_question(question=question,
                            input_widget=input_widget,
                            evaluation_function=evaluation_function)


def code_question(question: str, expected_outputs: list[tuple[tuple, Any]]) -> QuestionWidgetPackage:
    """
    Code question that uses a textbox for the user to write the name of a function.
    The provided function is tested against the expected_outputs.

    Delegates to generic_question.

    Parameters:
    - question: Question body
    - expected_output - a list of pairs in the format:
        - ((inputs), expected_output)
        - Example: [
            ((2, 4), 8)
        ]
    """

    input_widget = widgets.Text(
        description="What is the name of your function?", placeholder="myFunction",
        style=dict(description_width="initial"))

    def evaluation_function():
        function_name = input_widget.value
        if function_name not in globals():
            # Error handling
            return None

        function = globals()[function_name]
        return all([function(*test_input) == test_output
                    for test_input, test_output in expected_outputs])

    def feedback(evaluation_result):
        if evaluation_result is None:
            return "No function defined with that name. Remember to run the cell to define the function."
        if evaluation_result:
            return "Correct!"
        else:
            return "Incorrect answer!"

    return generic_question(question=question, input_widget=input_widget, evaluation_function=evaluation_function, feedback=feedback)


def no_input_question(question: str, solution: list[str]) -> QuestionWidgetPackage:
    """
    Questions with no input. 
    Reveals solution on button click if solution exists.

    Does not delegate to generic_question.

    Corresponds to the FaceIT question type: TEXT.
    """
    title_widget = question_title(question)

    if len(solution) == 0:
        # If no solution provided
        no_solution_widget = widgets.HTML(
            value="<p><i>This question has no suggested solution.</i></p>")
        return widgets.VBox([title_widget, no_solution_widget])

    # Solution has been provided

    solution_box = widgets.VBox(
        [widgets.HTMLMath(value=f"<p>{sol}</p>") for sol in solution])
    solution_box.layout.display = "none"  # Initially hidden

    def reveal_solution(button):
        if solution_box.layout.display == "none":
            solution_box.layout.display = "block"
            button.description = "Hide solution"
        else:
            solution_box.layout.display = "none"
            button.description = "Show solution"

    button = widgets.Button(description="Show solution", icon="check",
                            style=dict(
                                button_color="lightgreen"
                            ))

    button.on_click(reveal_solution)

    # Will always be considered a correct solution (does not influence score computation)
    always_correct = (lambda: True)

    # Will not give feedback, as there is no input
    no_feedback = (lambda: None)

    return widgets.VBox([title_widget, button, solution_box],
                        layout=dict(border_bottom="solid", border_top="solid",
                                    padding="0.2em")), always_correct, no_feedback
