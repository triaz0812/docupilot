const chatWindow = document.getElementById("chat-window");
const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");
const clearButton = document.getElementById("clear-chat");

const sanitizeText = (text) =>
    text.replace(/[&<>"']/g, (char) => (
        {
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            '"': "&quot;",
            "'": "&#39;",
        }[char]
    ));

const appendMessage = (role, text, { sources = [] } = {}) => {
    const wrapper = document.createElement("div");
    wrapper.className = `message ${role}`;

    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.innerHTML = sanitizeText(text).replace(/\n/g, "<br>");
    wrapper.appendChild(bubble);

    if (role === "assistant" && sources.length > 0) {
        const footer = document.createElement("div");
        footer.className = "sources";
        footer.innerHTML = "Sources: " + sources
            .map((source, index) => {
                const label = source.title || source.source || source.url || `Source ${index + 1}`;
                const href = source.source || source.url || "#";
                return `<a href="${href}" target="_blank" rel="noopener noreferrer">[${index + 1}] ${sanitizeText(label)}</a>`;
            })
            .join(" ");
        wrapper.appendChild(footer);
    }

    chatWindow.appendChild(wrapper);
    chatWindow.scrollTo({ top: chatWindow.scrollHeight, behavior: "smooth" });
};

const setLoading = (loading) => {
    chatInput.disabled = loading;
    chatForm.querySelector("button").disabled = loading;
};

const renderWelcome = () => {
    appendMessage("assistant", "Hello! How can I assist you today?");
};

chatForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const message = chatInput.value.trim();
    if (!message) {
        return;
    }

    appendMessage("user", message);
    chatInput.value = "";
    setLoading(true);

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message }),
        });

        if (!response.ok) {
            const payload = await response.json().catch(() => ({ detail: "Unexpected error" }));
            throw new Error(payload.detail || "Failed to fetch response");
        }

        const payload = await response.json();
        appendMessage("assistant", payload.answer, { sources: payload.sources });
    } catch (error) {
        appendMessage("assistant", `Critical Error: ${error.message}`);
    } finally {
        setLoading(false);
        chatInput.focus();
    }
});

clearButton.addEventListener("click", () => {
    chatWindow.innerHTML = "";
    renderWelcome();
    chatInput.focus();
});

renderWelcome();
