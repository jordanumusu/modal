import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/AppSidebar";

export default function AppLayout({ children }: { children: React.ReactNode }) {
  return (
      <div className="flex w-full">
        <main className="flex-1">{children}</main>
      </div>
  );
}
