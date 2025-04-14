import { create } from "zustand";

export type ChatMessage = {
  sender: "user" | "llm";
  content: string;
  response_id?: string;
};

type ChatStore = {
  chatHistory: ChatMessage[];
  query: string;
  addChatMessage: (message: ChatMessage) => void;
  setQuery: (query: string) => void;
  clearChat: () => void;
};

export const useChatStore = create<ChatStore>((set) => ({
  chatHistory: [],
  query: "",
  addChatMessage: (message) =>
    set((state) => ({
      chatHistory: [...state.chatHistory, message],
    })),  setQuery: (query) => set(() => ({ query })),
  clearChat: () => set(() => ({ chatHistory: [], query: "" })),
}));
