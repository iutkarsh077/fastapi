import { Router } from "express";
import ChatResponse from "../controller/ChatResponse.js";

const router = Router();

router.get("/chat", ChatResponse);

export default router