#!/usr/bin/env python3
"""Claude Code usage in the macOS menu bar.

Shows remaining 5-hour and weekly token budget (same numbers as the
official /usage command) as a menu bar title, with a dropdown for details.
No Windows, no browser tab — just reads local Claude Code state.

Run:
  .venv/bin/python app.py
"""
import rumps

import claude_stats

REFRESH_SECONDS = 60


class ClaudeTrayApp(rumps.App):
    def __init__(self):
        super().__init__("Claude Usage", title="…")
        self.item_model = rumps.MenuItem("Модель: —")
        self.item_cost = rumps.MenuItem("Сессия: —")
        self.item_burn = rumps.MenuItem("Скорость: —")
        self.item_window = rumps.MenuItem("5 часов: —")
        self.item_weekly = rumps.MenuItem("Неделя: —")
        self.item_source = rumps.MenuItem("Источник: —")
        self.menu = [
            self.item_window,
            self.item_weekly,
            None,
            self.item_model,
            self.item_cost,
            self.item_burn,
            self.item_source,
            None,
            rumps.MenuItem("Обновить сейчас", callback=self.refresh),
        ]
        self.refresh(None)
        self.timer = rumps.Timer(self.refresh, REFRESH_SECONDS)
        self.timer.start()

    def refresh(self, _sender):
        try:
            stats = claude_stats.parse_stats()
        except Exception as e:
            self.title = "Claude: err"
            self.item_source.title = f"Источник: ошибка ({e})"
            return

        h_left = 100 - stats["window_pct"]
        w_left = 100 - stats["weekly_pct"]
        self.title = f"h {h_left:.0f}% · w {w_left:.0f}%"

        self.item_window.title = (
            f"5 часов: {h_left:.0f}% осталось"
            + (f" · сброс {stats['window_reset']}" if stats["window_reset"] else "")
        )
        self.item_weekly.title = (
            f"Неделя: {w_left:.0f}% осталось"
            + (f" · сброс {stats['weekly_reset']}" if stats["weekly_reset"] else "")
        )
        self.item_model.title = f"Модель: {stats['model']}"
        self.item_cost.title = f"Сессия: ${stats['cost']:.2f}"
        activity = (
            f"{stats['burn_rate']:.0f} tok/min" if stats["burn_rate"] > 0
            else ("печатает…" if stats["is_active"] else "простой")
        )
        self.item_burn.title = f"Активность: {activity}"
        self.item_source.title = (
            "Источник: Anthropic API (точно)" if stats["api_ok"]
            else "Источник: оценка по логам (офлайн)"
        )


if __name__ == "__main__":
    ClaudeTrayApp().run()
