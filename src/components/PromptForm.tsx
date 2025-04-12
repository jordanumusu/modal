import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Search } from "lucide-react"

export function PromptForm() {
  return (
    <form className="flex items-center gap-2 w-[50%]">
      <div className="relative w-full">
      <Search className="pointer-events-none absolute left-2 top-1/4 size-4 -translate-y-1/2 select-none opacity-50" />
      <Input
          className="pl-9"
          placeholder="Ask something..."
        />
      </div>

      <Button type="submit">
        Search
      </Button>
    </form>
  )
}
