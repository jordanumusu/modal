"use client"

import { SquarePen } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useChatStore } from "@/store/chatStore";

export function NewChatButton() {
  const { clearChat } = useChatStore();
  return (
    <Button onClick={clearChat}>
      <SquarePen /> New Chat
    </Button>
  );
}
