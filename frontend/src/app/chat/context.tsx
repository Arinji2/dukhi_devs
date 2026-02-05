import { PulseIcon } from "@/components/icons/pulse";

<div className="flex h-full w-[40%] flex-col gap-5 bg-background px-4 py-6">
  <div className="flex h-fit w-full flex-col items-start justify-start gap-1 rounded-sm bg-card p-4">
    <div className="flex h-fit w-full flex-row items-center justify-start gap-1">
      <PulseIcon className="size-5 text-pastel-green" />
      <p className="font-content font-semibold text-muted-foreground text-xs tracking-tight">
        SENSITIVITY LEVEL
      </p>
    </div>
    <div className="flex h-fit w-full flex-row items-center justify-start gap-2">
      <div className="flex h-2 w-full flex-row items-center justify-start overflow-hidden rounded-md border border-border">
        <div className="h-full w-[80%] bg-secondary"></div>
      </div>
      <p className="font-semibold text-[10px] text-secondary tracking-tight">
        High
      </p>
    </div>

    <p className="font-light text-[11px] text-muted-foreground">
      Immediate attention recommended due to potential emotional distress and
      hostile environment.
    </p>
  </div>
  <div className="flex h-fit w-full flex-col items-start justify-start gap-3 rounded-sm bg-card p-4">
    <div className="flex h-fit w-full flex-row items-center justify-start gap-1">
      <PulseIcon className="size-5 text-pastel-green" />
      <p className="font-content font-semibold text-muted-foreground text-xs tracking-tight">
        VICTIM PROFILE
      </p>
    </div>
    <div className="flex h-fit w-full flex-row items-center justify-between gap-2">
      <div className="flex h-fit w-fit flex-col items-start justify-start gap-1">
        <p className="font-medium text-[10px] text-muted-foreground">
          AGE GROUP
        </p>
        <p className="font-medium text-foreground text-sm">Adult (Working)</p>
      </div>
      <div className="flex h-fit w-fit flex-col items-start justify-start gap-1">
        <p className="font-medium text-[10px] text-muted-foreground">ROLE</p>
        <p className="font-medium text-foreground text-sm">Employee</p>
      </div>
    </div>
  </div>
  <div className="flex h-fit w-full flex-col items-start justify-start gap-3 rounded-sm bg-card p-4">
    <div className="flex h-fit w-full flex-row items-center justify-start gap-1">
      <PulseIcon className="size-5 text-pastel-green" />
      <p className="font-content font-semibold text-muted-foreground text-xs tracking-tight">
        SITUATION CONTEXT
      </p>
    </div>
    <div className="flex h-fit w-fit flex-col items-start justify-start gap-1">
      <p className="font-medium text-[10px] text-muted-foreground">SETTING</p>
      <p className="font-medium text-foreground text-sm"></p>
    </div>
  </div>
</div>;
