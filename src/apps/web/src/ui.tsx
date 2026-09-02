import type { ReactNode, SVGProps } from "react";

export type IconName =
  | "activity"
  | "arrow-right"
  | "audit"
  | "chart"
  | "check"
  | "chevron-right"
  | "cases"
  | "dashboard"
  | "play"
  | "refresh"
  | "shield"
  | "spark"
  | "terminal"
  | "warning";

type IconProps = SVGProps<SVGSVGElement> & {
  name: IconName;
  size?: number;
};

export function Icon({ name, size = 18, ...props }: IconProps) {
  const paths: Record<IconName, ReactNode> = {
    activity: <path d="M3 12h3l2.1-6 4 12 2.1-6H21" />,
    "arrow-right": <path d="M5 12h14m-6-6 6 6-6 6" />,
    audit: <><path d="M6 3h9l3 3v15H6z" /><path d="M15 3v4h4M9 12h6M9 16h6" /></>,
    cases: <><rect x="3" y="4" width="18" height="16" rx="2" /><path d="M7 8h10M7 12h4M7 16h7" /></>,
    chart: <><path d="M4 19V5M4 19h17" /><path d="m7 15 4-4 3 2 5-6" /></>,
    check: <path d="m5 12 4.2 4.2L19 6.5" />,
    "chevron-right": <path d="m9 18 6-6-6-6" />,
    dashboard: <><rect x="3" y="3" width="7" height="7" rx="1" /><rect x="14" y="3" width="7" height="7" rx="1" /><rect x="3" y="14" width="7" height="7" rx="1" /><rect x="14" y="14" width="7" height="7" rx="1" /></>,
    play: <path d="m8 5 11 7-11 7z" />,
    refresh: <><path d="M20 11a8 8 0 0 0-14.9-3L3 10" /><path d="M3 4v6h6M4 13a8 8 0 0 0 14.9 3L21 14" /><path d="M21 20v-6h-6" /></>,
    shield: <path d="M12 3 4.5 6v5.7c0 4.6 3.1 7.6 7.5 9.3 4.4-1.7 7.5-4.7 7.5-9.3V6zM8.7 12l2.2 2.2 4.5-4.5" />,
    spark: <path d="m12 2 1.7 6.3L20 10l-6.3 1.7L12 18l-1.7-6.3L4 10l6.3-1.7zM19 17l.6 2.4L22 20l-2.4.6L19 23l-.6-2.4L16 20l2.4-.6z" />,
    terminal: <><path d="m5 7 4 4-4 4M11 17h8" /><rect x="3" y="3" width="18" height="18" rx="2" /></>,
    warning: <><path d="m12 3 9 16H3z" /><path d="M12 9v4M12 17h.01" /></>,
  };

  return (
    <svg
      aria-hidden="true"
      fill="none"
      height={size}
      stroke="currentColor"
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={1.8}
      viewBox="0 0 24 24"
      width={size}
      {...props}
    >
      {paths[name]}
    </svg>
  );
}

export function formatCurrency(value: number | null | undefined) {
  if (value === null || value === undefined) return "—";
  return new Intl.NumberFormat("en-IN", {
    currency: "INR",
    maximumFractionDigits: 0,
    style: "currency",
  }).format(value / 100);
}

export function titleCase(value: string | null | undefined) {
  if (!value) return "—";
  return value.replaceAll("_", " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
}

export function StatusPill({ children, tone = "neutral" }: { children: ReactNode; tone?: "good" | "neutral" | "warn" }) {
  return <span className={`status-pill status-pill--${tone}`}>{children}</span>;
}

export function EmptyState({ detail, icon = "cases", title }: { detail: string; icon?: IconName; title: string }) {
  return (
    <div className="empty-state">
      <span className="empty-state__icon"><Icon name={icon} size={22} /></span>
      <div>
        <strong>{title}</strong>
        <p>{detail}</p>
      </div>
    </div>
  );
}
