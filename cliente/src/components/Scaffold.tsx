import { Outlet } from "react-router";

export default function Scaffold({ TopBar, BottomBar, children }: any) {
  return (
    <div className="w-full h-svh flex flex-col overflow-hidden">
      {TopBar && TopBar}
      <main className="flex-1 overflow-y-auto">
        {children ? children : <Outlet />}
      </main>
      {BottomBar && BottomBar}
    </div>
  );
}
