# ============================================
# HydraPlexus (Heart) — Truth Through Erasure
# No time. No replay. No logs.
# ============================================
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, Literal
import json, hashlib

# =========================
# Crown Membrane (3-gem plane)
# =========================
# Numeric cycle is the protocol; names are lore.
GEMS = {1: "ONYX", 2: "JADE", 3: "OPAL"}
def gem_name(g: int) -> str: return GEMS.get(int(g or 1), "G?")

# =========================
# Crown Coil (conductive ventricular cycling)
# =========================
def crown_coil_next(c: int) -> int: return 1 if int(c) >= 3 else int(c) + 1
next_gem = next_crown = crown_coil_next  # Back-compat names (demo / earlier drafts)

# =========================
# Nexus Tip (identity derives from full state)
# =========================
def nexus_tip_hash(tallies: Dict[str, int], crown: int) -> str:
    obj = {"tallies": dict(tallies), "crown": int(crown)}
    b = json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(b).hexdigest()[:12]
state_hash = nexus_tip_hash  # Back-compat name

def limbic_key(tail: Dict[str, Any]) -> Tuple[int, str, str]:
    return (int(tail.get("weight", 0)), str(tail.get("id", "")), str(tail.get("h", "")))
collapse_key = limbic_key  # Back-compat name

# =========================
# Crown Ventricles (proposal secretion)
# =========================
def crown_ventricles_emit_tail(head_id: str, tallies_snapshot: Dict[str, int], crown_snapshot: int, tx: Tuple[str, str, int]) -> Dict[str, Any]:
    frm, to, amt = tx
    tallies = dict(tallies_snapshot)
    tallies[frm] = tallies.get(frm, 0) - int(amt)
    tallies[to] = tallies.get(to, 0) + int(amt)
    crown = crown_coil_next(int(crown_snapshot))
    h = nexus_tip_hash(tallies, crown)
    return {"id": head_id, "tallies": tallies, "crown": crown, "weight": int(h, 16), "h": h}
cortex_emit_tail = crown_ventricles_emit_tail  # Back-compat name

# ====================================
# Apex Ventricle (HydraPlex → Body)
# =========================
IntentType = Literal["PROPAGATE", "REQUEST_SYNC", "ENVY"]
@dataclass(frozen=True)
class Intent:
    type: IntentType
    payload: Dict[str, Any]

# =========================
# HydraPlex (sealed heart)
# =========================
@dataclass
class HydraState:
    tallies: Dict[str, int]
    crown: int
    h: Optional[str] = None
    head: Optional[str] = None

class HydraPlexus:
    def __init__(self, head_id: str, initial_tallies: Optional[Dict[str, int]] = None, initial_crown: int = 1) -> None:
        self.head_id = str(head_id)
        self.state = HydraState(
            tallies=dict(initial_tallies or {"A": 10, "B": 10, "C": 10, "D": 10, "E": 10}),
            crown=int(initial_crown),
            h=None, head=None,
        )
        self.tail: Optional[Dict[str, Any]] = None
        self.envy: bool = False

    # -------------------------
    # Crown Ventricles (proposal)
    # -------------------------
    def propose(self, to_head: str, amount: int) -> Dict[str, Any]:
        return crown_ventricles_emit_tail(self.head_id, dict(self.state.tallies), int(self.state.crown), (self.head_id, str(to_head), int(amount)))

    # =========================
    # Limbic Dream State
    # =========================
    def dream_state(self) -> Dict[str, Any]:
        tail = {"id": (self.state.head or self.head_id), "tallies": dict(self.state.tallies), "crown": int(self.state.crown), "weight": 0}
        tail["h"] = nexus_tip_hash(tail["tallies"], tail["crown"])
        tail["weight"] = int(tail["h"], 16)
        return tail
    snapshot_tail = dream_state  # Back-compat alias

    def snapshot(self) -> Dict[str, Any]:
        return {"tallies": dict(self.state.tallies), "crown": int(self.state.crown), "h": self.state.h, "head": self.state.head}
    def emotions(self) -> Dict[str, Any]: return {"envy": bool(self.envy)}

    # -------------------------
    # Crown Membrane → Nexus Tip
    # -------------------------
    def _at_nexus_tip(self, tail_in: Dict[str, Any]) -> Dict[str, Any]:
        incoming_tallies = dict(tail_in.get("tallies", {}) or {})
        incoming_crown = int(tail_in.get("crown", 1))
        h = nexus_tip_hash(incoming_tallies, incoming_crown)
        out = dict(tail_in)
        out.update({"tallies": incoming_tallies, "crown": incoming_crown, "h": h, "weight": int(h, 16)})
        return out

    # -------------------------
    # Limbic Core (survival law)
    # -------------------------
    def ingest(self, tail_in: Dict[str, Any]) -> List[Intent]:
        intents: List[Intent] = []
        tail_in = self._at_nexus_tip(tail_in)
        inc_tallies, inc_crown, inc_h = dict(tail_in["tallies"]), int(tail_in["crown"]), str(tail_in["h"])

        # --- Hold: detect stalemate
        if inc_h and inc_h == self.state.h: return intents

        # ---First Gasp: uninitialized heart
        if self.state.h is None:
            self.state.tallies, self.state.crown, self.state.h = dict(inc_tallies), inc_crown, inc_h
            self.state.head = str(tail_in.get("id", "")) or None
            self.tail = dict(tail_in); self.tail["h"] = self.state.h
            self.envy = False
            intents.append(Intent("PROPAGATE", {"tail": dict(self.tail)}))
            intents.append(Intent("REQUEST_SYNC", {"crown": self.state.crown, "need_tail": False, "gem": gem_name(self.state.crown)}))
            return intents

        cur = int(self.state.crown or 1)
        exp = crown_coil_next(cur)

        # --- Crown Gate (membrane admissibility)
        if inc_crown not in (cur, exp):
            self.envy = True
            intents.append(Intent("ENVY", {"current_crown": cur, "incoming_crown": inc_crown}))
            intents.append(Intent("REQUEST_SYNC", {"crown": cur, "need_tail": True, "gem": gem_name(cur)}))
            return intents

        # --- Tighten: apply pressure
        should_adopt = (inc_crown == exp) or (inc_crown == cur and limbic_key(tail_in) > limbic_key(self.tail or self.dream_state()))
        if not should_adopt: return intents

        advanced = (inc_crown == exp)
        self.state.tallies, self.state.crown, self.state.h = dict(inc_tallies), inc_crown, inc_h
        self.state.head = str(tail_in.get("id", "")) or None
        self.tail = dict(tail_in); self.tail["h"] = self.state.h

        # --- Apex Ventricle → body
        intents.append(Intent("PROPAGATE", {"tail": dict(self.tail)}))
        if advanced:
            intents.append(Intent("REQUEST_SYNC", {"crown": inc_crown, "need_tail": False, "gem": gem_name(inc_crown)}))
        return intents
