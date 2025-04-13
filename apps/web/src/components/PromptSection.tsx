'use client'
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { ChevronRight } from "lucide-react";
import { z } from "zod";

export function PromptSection() {
  const handleSubmit = async (e) => {
    e.preventDefault()

    // Extract query value directly from the form
    const query = e.target.query.value;

    // Send the form data to the API using fetch
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/generate-answer`, {
      method: "POST",
      body: JSON.stringify({ query }), // Send as JSON object
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (response.ok) {
      // Handle success (e.g., parse the response)
      const data = await response.json();
      console.log(data);
    } else {
      // Handle error response
      console.error("Failed to submit form", response);
    }
  };

  return (
    <div className="flex flex-col h-full w-full p-4 items-center">
      <div className="flex-1 overflow-y-auto"></div>
      <div className="w-full sticky bottom-0 flex justify-center max-h-48">
        <form onSubmit={handleSubmit} className="w-[50%]">
          <div className="relative overflow-y-auto w-full h-full border-2 p-4 rounded-lg focus:ring-2 focus:ring-blue-500 flex items-center justify-between">
            {/* Textarea TODO: Fix styling*/}

            <Textarea
              className="max-w-96flex-1 text-lg border-none resize-y min-h-[25px]"
              name="query"
              placeholder="Ask me anything..."
            />
            <Button type="submit" className="rounded-full" size="icon">
              <ChevronRight className="size-5" />
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}
