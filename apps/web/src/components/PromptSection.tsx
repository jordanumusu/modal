"use client";

import { useChatStore } from "@/store/chatStore";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { ChevronRight } from "lucide-react";
import { useEffect, useRef, FormEvent, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import ReactMarkdown from "react-markdown";

export function PromptSection() {
  const { chatHistory, addChatMessage, query, setQuery } = useChatStore();
  const [isLoading, setIsLoading] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }
  }, [chatHistory]);

  useEffect(() => {
    console.log(chatHistory);
  }, [chatHistory]);

  const getLatestResponseId = () => {
    const llmMessages = chatHistory.filter((msg) => msg.sender === "llm");
    return llmMessages.length > 0
      ? llmMessages[llmMessages.length - 1].response_id
      : null;
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    addChatMessage({ sender: "user", content: query });
    setQuery("");
    setIsLoading(true);

    const latestResponseId = getLatestResponseId();

    const requestBody = {
      query,
      ...(latestResponseId && { prev_response_id: latestResponseId }),
    };

    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_URL}/api/generate-answer`,
      {
        method: "POST",
        body: JSON.stringify(requestBody),
        headers: {
          "Content-Type": "application/json",
        },
      }
    );

    if (response.ok) {
      const data = await response.json();
      addChatMessage({
        sender: "llm",
        response_id: data.id,
        content: data.output,
      });
    } else {
      console.error("Failed to submit form", response);
    }
    setIsLoading(false);
  };

  const handleKeyDown = async (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const splitMessageIntoChunks = (message: string) => {
    return message.split(". ").map((chunk) => chunk.trim() + ".");
  };

  return (
    <div className="flex flex-col h-full w-full p-4 items-center">
      <div ref={containerRef} className="w-[70%] sm:w-[60%] flex-1 overflow-y-auto scrollbar-thin scrollbar-thumb-muted scrollbar-track-transparent overflow-x-hidden flex flex-col gap-8 pb-16">
        {chatHistory.map((message, index) =>
          message.sender === "user" ? (
            <div key={index} className="flex justify-end">
              <div className="flex text-left max-w-lg leading-1.5 px-4 py-2 border-gray-200 bg-zinc-300 rounded-xl rounded-tr-none dark:bg-zinc-600">
                <p className="text-sm font-normal py-2.5 text-gray-900 dark:text-white">
                  {message.content}
                </p>
              </div>
            </div>
          ) : (
            <div key={index} className="text-lg">
              <Card className="shadow-md bg-zinc-100 dark:bg-zinc-900">
                <CardContent>
                  {splitMessageIntoChunks(message.content).map(
                    (chunk, chunkIndex, allChunks) => (
                      <p
                        key={chunkIndex}
                        className="opacity-0 animate-typewriter"
                        style={{
                          animationDelay: `${chunkIndex * 0.3}s`,
                          animationFillMode: "forwards",
                        }}
                      >
                        <ReactMarkdown>{chunk}</ReactMarkdown>
                      </p>
                    )
                  )}
                </CardContent>
              </Card>
            </div>
          )
        )}
        {isLoading && (
          <div className="text-lg">
            <Card>
              <CardContent className="animate-pulse space-y-2">
                <div className="h-4 w-3/4 bg-muted rounded" />
                <div className="h-4 w-1/2 bg-muted rounded" />
                <div className="h-4 w-2/3 bg-muted rounded" />
              </CardContent>
            </Card>
          </div>
        )}

        {chatHistory.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full text-center animate-intro text-2xl font-semibold text-muted-foreground p-4">
            <p className="text-2xl sm:text-3xl font-semibold flex gap-2">
              {["🎶", "Welcome", "to", "Modal"].map((word, i) => (
                <span
                  key={i}
                  className="text-primary inline-block animate-word-bounce"
                  style={{
                    animationDelay: `${i * 0.15}s`,
                  }}
                >
                  {word}
                </span>
              ))}
            </p>
            <p className="text-base mt-2 font-normal">
              Your AI assistant for chord progressions, solos, song ideas, and
              more.
            </p>
          </div>
        )}
      </div>

      <div className="w-full fixed bottom-0 flex justify-center max-h-64 pb-8">
        <form onSubmit={handleSubmit} className="w-[80%] sm:w-[50%]">
          <div className="relative scrollbar-thin scrollbar-thumb-muted scrollbar-track-transparent overflow-y-auto w-full h-full border-2 p-4 rounded-lg flex gap-2 items-center justify-between bg-background">
            <Textarea
              rows={1}
              className="dark:bg-grey-800 resize-none max-w-full flex-1 text-xl border-none min-h-[25px]"
              name="query"
              value={query}
              onKeyDown={handleKeyDown}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask me anything..."
            />
            <Button
              type="submit"
              className="rounded-full cursor-pointer"
              size="icon"
            >
              <ChevronRight className="size-5" />
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}
