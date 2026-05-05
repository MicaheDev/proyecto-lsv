import { Outlet } from "react-router";

export default function Scaffold({ TopBar, BottomBar }: any) {
  return (
    <div className="w-full h-svh flex flex-col overflow-hidden">
      {TopBar && TopBar}
      <main className="flex-1 bg-red-500 overflow-y-auto">
        <Outlet />
      </main>
      {BottomBar && BottomBar}
    </div>
  );
}
