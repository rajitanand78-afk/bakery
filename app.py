import gradio as gr
from bakery_message_starter import analyse, classify, keywords, message_score
COLORS = {"urgent": "salmon"}
def check(message):
    pieces = []
    for word, points in analyse(message):
        label = "urgent" if points > 0 else None
        pieces.append((word + " ", label))
    keyword_list = ", ".join(keywords(message)) or "No urgency words found"
    return classify(message), message_score(message), keyword_list, pieces
demo = gr.Interface(
    fn=check,
    inputs=gr.Textbox(lines=3, label="Bakery message"),
    outputs=[
        gr.Textbox(label="Priority"),
        gr.Number(label="Urgency score"),
        gr.Textbox(label="Urgency keywords"),
        gr.HighlightedText(label="Tokenized message", color_map=COLORS),
    ],
    title="Bakery Message Sorter",
    description="Messages scoring 2 or more are URGENT. Other messages are NORMAL.",
    examples=[
        ["My cake is needed today, please call me ASAP"],
        ["Can you send me the bread menu?"],
        ["The delivery is delayed and my order is late"],
    ],
)
if __name__ == "__main__":
    demo.launch()
