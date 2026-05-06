import {
  FireIcon,
  HeartIcon,
  ShieldIcon,
  StarIcon,
} from "@phosphor-icons/react";

export default function TopBar() {
  return (
    <div className="h-15 w-full flex justify-between items-center px-6">
      <button className="flex items-center gap-1">
        <ShieldIcon
          weight="fill"
          stroke="black"
          strokeWidth={10}
          className="text-emerald-300"
          size={30}
        />
        <span className="font-black uppercase">A1</span>
      </button>
      <button className="flex items-center gap-1 opacity-25">
        <FireIcon
          weight="fill"
          stroke="black"
          strokeWidth={10}
          className="text-orange-400"
          size={30}
        />
        <span className="font-black">0</span>
      </button>

      <button className="flex items-center gap-1">
        <StarIcon
          weight="fill"
          stroke="black"
          strokeWidth={10}
          className="text-yellow-400"
          size={30}
        />
        <span className="font-black">100</span>
      </button>
      <button className="flex items-center gap-1">
        <HeartIcon
          weight="fill"
          stroke="black"
          strokeWidth={10}
          className="text-red-400"
          size={30}
        />
        <span className="font-black">5</span>
      </button>
    </div>
  );
}
