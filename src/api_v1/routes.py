import csv
from typing import Annotated

from fastapi import APIRouter, HTTPException, Body
from src.database.models import Player, PlayerLevel, Level
from src.schemas import PlayerSchema, LevelCompleteRequest


router = APIRouter(prefix='/api/v1')


@router.get('/player', response_model=PlayerSchema)
async def get_player(player_id: str):

    player = await Player.get_player_by_id(player_id)

    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    return player


@router.post('/give-out-prize')
async def give_out_prize(request: Annotated[LevelCompleteRequest, Body()]):
    player_id = request.player_id
    player = await Player.get_player_by_id(str(player_id))

    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    order = request.order
    levels = [level.level.order for level in player.player_levels]

    if order in levels:
        raise HTTPException(status_code=403, detail="The level has already been completed")

    target_level = await Level.get_level_by_order(order)

    if not target_level:
        raise HTTPException(status_code=403, detail="Level not found")

    score = request.score
    await PlayerLevel.create_player_level(player.id, score, target_level.id)

    return {"status": True}


@router.get('/load-database')
async def load_database_in_csv():
    result = await Player.get_all_notes()
    filename = "./assets/players.csv"
    fields = ['player_id', 'Уровень', 'Пройден?', 'Приз']

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)

        for player in result:
            if player:
                player_id = player.player_id
                player_levels = player.player_levels

                if player_levels:
                    for level in player_levels:
                        is_completed = level.is_completed
                        name_level = level.level.title
                        prize = level.level.level_prizes[0].prize.title if level.level.level_prizes else ''

                        csvwriter.writerow([player_id, name_level, is_completed, prize])
                else:
                    name_level = ''
                    is_completed = ''
                    prize = ''
                    csvwriter.writerow([player_id, name_level, is_completed, prize])

    return result
