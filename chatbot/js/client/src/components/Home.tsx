import { useEffect, useRef, useState } from "react";
import api from "../helpers/api";

interface IConversation {
  me: string;
  ai: string;
}

const Home = () => {
  const [conversation, setConversation] = useState<IConversation[]>([]);
  const [text, setText] = useState("");
  const refContainer = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (!refContainer.current) return;

    refContainer.current.scrollTo({
      top: refContainer.current.scrollHeight,
      behavior: "smooth",
    });
  }, [conversation]);

  const handleSendRequest = async () => {
    if (!text.trim()) return;

    try {
      const response = await api.get("/chat", { params: { question: text } });

      if (response.status != 201) {
        throw new Error("Request failed!");
      }
      setConversation((prev) => [
        ...prev,
        { me: text, ai: response.data.data },
      ]);
      setText("");
    } catch (error) {
      console.log(error);
      alert("Internal Server error, please try again!");
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      handleSendRequest();
    }
  };

  return (
    <div className="w-full h-screen bg-black flex flex-col items-center">
      <div
        ref={refContainer}
        className="w-full max-w-4xl flex-1 overflow-y-auto px-4 py-8 pb-24"
      >
        {conversation.length === 0 ? (
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <h1 className="text-4xl font-bold text-white mb-4">
                Chat Assistant
              </h1>
              <p className="text-gray-400 text-lg">
                Start a conversation by typing a message below
              </p>
            </div>
          </div>
        ) : (
          <div className="space-y-6">
            {conversation.map((item: IConversation, index: number) => (
              <div key={index} className="space-y-4">
                {/* User Message */}
                <div className="flex justify-end">
                  <div className="bg-white text-black px-6 py-3 rounded-2xl rounded-tr-sm max-w-2xl">
                    <p className="text-base leading-relaxed">{item.me}</p>
                  </div>
                </div>

                {/* AI Message */}
                <div className="flex justify-start">
                  <div className="bg-gray-900 text-white px-6 py-3 rounded-2xl rounded-tl-sm max-w-2xl border border-gray-800">
                    <p className="text-base leading-relaxed">{item.ai}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="fixed bottom-0 left-0 right-0 bg-linear-to-t from-black via-black to-transparent py-4">
        <div className="max-w-3xl mx-auto px-4">
          <div className="flex items-center gap-3 bg-gray-900 rounded-full border-2 border-gray-700 focus-within:border-white transition-colors p-2">
            <input
              value={text}
              onChange={(e) => setText(e.target.value)}
              onKeyDown={handleKeyPress}
              type="text"
              placeholder="Ask a question..."
              className="flex-1 bg-transparent text-white px-4 py-3 text-base outline-none placeholder-gray-500"
            />
            <button
              onClick={handleSendRequest}
              type="button"
              disabled={!text.trim()}
              className="bg-white text-black px-8 py-3 font-semibold rounded-full hover:bg-gray-200 active:scale-95 transition-all disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-white disabled:active:scale-100"
            >
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
