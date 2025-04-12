import { PromptForm } from "@/components/PromptForm";
export function PromptSection() {
  return (
    <div className="flex flex-col h-full w-full p-4 items-center">
      <div className="flex-1 overflow-y-auto"></div>
      <PromptForm />
    </div>
  );
}
