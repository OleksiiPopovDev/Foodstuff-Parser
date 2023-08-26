from database.connector import Connector
from dto.category_dto import CategoryDto
from database.model.category_model import Category
from database.model.statistic_model import Statistic
from repository.statistic_status import StatisticStatus


class CategoryRepository(Connector):
    @staticmethod
    def save(category_dto: CategoryDto) -> None:
        Category.create(
            page=category_dto.page,
            store=category_dto.store_id,
            product_count=category_dto.product_count,
            source=category_dto.source
        )

    @staticmethod
    def list() -> list[CategoryDto]:
        data = (
            Category
            .select()
            .join(
                Statistic,
                on=((Category.page == Statistic.category) & (Category.store == Statistic.store)),
                join_type='LEFT JOIN'
            )
            .where(
                (Statistic.status == StatisticStatus.IN_PROGRESS.value) |
                Statistic.status.is_null()
            )
            .order_by(Statistic.status.desc()))

        categories: list[CategoryDto] = []
        for category in data:
            categories.append(CategoryDto(
                id=category.id,
                page=str(category.page),
                store_id=category.store.id,
                product_count=int(category.product_count),
                source=category.source
            ))

        return categories
